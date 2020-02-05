# -*- coding: utf-8 -*-

"""User module."""
import logging
from datetime import datetime

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class ArcherDB:
    """Creates archer db instance object using following arguments.

    Args:
        username (str): Username for database connection.
        password (str): Password for database connection.
        host (str): Host for database connection.
        instance_database (str): Database name for the "Instance"
        configuration_database (str): Database name for the "Configuration"

    Kwargs:
        port (optional, int): Port for database connection.
            Default: 5432
        drivername (optional, str): Driver to use for connection.
            Default: mssql+pyodbc

    Attributes:
        inst_engine (sqlalchemy.create_engine): Engine used for connecting to
            the instance database
        conf_engine (sqlalchemy.create_engine): Engine used for connecting to
            the configuration database
        conf_metadata (sqlalchemy.MetaData)
        conf_session (sqlalchemy.orm.sessionmaker)
        inst_metadata (sqlalchemy.MetaData)
        inst_session (sqlalchemy.orm.sessionmaker)
    """

    def __init__(self, *args, **kwargs):
        """Init."""
        instance_db_creds = dict(
            username=args[0],
            password=args[1],
            host=args[2],
            database=args[3],
            port=kwargs.get("port", 1433),
            drivername=kwargs.get("drivername", "mssql+pyodbc"),
            query=kwargs['query']
        )
        configuration_db_creds = dict(
            username=args[0],
            password=args[1],
            host=args[2],
            database=args[4],
            port=kwargs.get("port", 1433),
            drivername=kwargs.get("drivername", "mssql+pyodbc"),
            query=kwargs['query']
        )

        self.inst_engine = create_engine(URL(**instance_db_creds))
        self.conf_engine = create_engine(
            URL(**configuration_db_creds)
        )

        self.conf_metadata = MetaData(bind=self.conf_engine)
        conf_session_maker = sessionmaker(bind=self.conf_engine)
        self.conf_session = conf_session_maker()

        self.inst_metadata = MetaData(bind=self.inst_engine)
        inst_session_maker = sessionmaker(bind=self.inst_engine)
        self.inst_session = inst_session_maker()

    def get_table(
        self,
        table_name: str,
        database: str = "Instance"
    ) -> Table:
        """sqlalchemy.table object based on name.

        Args:
            table_name (str): Table name

        Kwargs:
            database (str): Specify either Instance or Configuration database

        Rerturns:
            sqlalchemy.Table
        """
        if database.lower() == "instance":
            return Table(
                table_name,
                self.inst_metadata,
                autoload=True,
                autoload_with=self.inst_engine
            )
        return Table(
                table_name,
                self.conf_metadata,
                autoload=True,
                autoload_with=self.conf_engine
            )

    def get_job_tables(self, query: bool = True) -> dict:
        """List of static tables used for Job Engine.

        Kwargs:
            query (bool): Weather to return the raw list of sqlalchemy Table or
                to return the session query of each table.

        Returns:
            dict
        """
        tables = {
            "tblAsyncJobQueue": self.get_table("tblAsyncJobQueue"),
            "tblAsyncJobHold": self.get_table("tblAsyncJobHold"),
            "tblAsyncJobProgress": self.get_table("tblAsyncJobProgress"),
            "tblJobStatus": self.get_table("tblJobStatus")
        }
        if query:
            data = {}
            for table_name in tables:
                table = tables[table_name]
                if table_name == "tblJobStatus":
                    data.update({
                        table_name: self.inst_session.query(table).filter(
                            table.c.job_status_id == 1
                        )
                    })
                elif table_name == "tblAsyncJobQueue":
                    data.update({
                        table_name: self.inst_session.query(table).filter(
                            table.c.InactiveUntil < datetime.now()
                        )
                    })
                else:
                    data.update({
                        table_name: self.inst_session.query(table)
                    })
            return data
        return tables

    def get_jobs_counts(self) -> dict:
        """Get Jobs.

        Returns:
            dict: table names and counts
        """
        tables = self.get_job_tables()
        data = {}
        for table_name in tables:
            table = tables[table_name]
            count = table.count()
            logging.info(
                "Table %s has %s jobs",
                table_name,
                count
            )
            data.update({table_name: count})
        return data

    def discontinue_job_processing(self, property_value=True):
        """Change the job engine to discontinue job processing."""
        table = self.get_table("tblProperty", database="Configuration")
        self.conf_session.query(table).filter(
            table.c.property_key.like('IsDequeuingDisabled')
        ).update({
            table.c.property_value: str(property_value)
        }, synchronize_session=False)

        self.conf_session.commit()

    def kill_all_jobs(self):
        """Kills all Archer jobs."""
        tables = self.get_job_tables()
        counts = self.get_jobs_counts()
        tables_with_counts = {
            count: counts[count] for count in counts if counts[count] > 0
        }
        if not tables_with_counts:
            logging.info("No jobs in queue.")
            return
        for table_name in tables_with_counts:
            if counts[table_name] == 0:
                continue
            table = tables[table_name]
            data = table.all()
            with self.inst_engine.begin() as connection:
                for row in data:
                    row_dict = row._asdict()

                    job_id = (
                        row_dict.get('JobId') or
                        row_dict.get("TargetJobId") or
                        row_dict.get("job_progress_id") or
                        row_dict.get("job_id")
                    )
                    endpoint = "ARCHERCOMPUTER"
                    query = (
                        "exec usp_async_job_queue_remove_running_job "
                        "'{}', '{}'".format(
                            job_id,
                            endpoint
                        )
                    )
                    connection.execute(query)
                    logging.info(query)
