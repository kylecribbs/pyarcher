job_info = {
    "general": {
        "configure": [
            "IF OBJECT_ID('tempdb..#jobDetail') IS NOT NULL DROP TABLE #jobDetail",
            """
            CREATE TABLE #jobDetail (
                jobid UNIQUEIDENTIFIER
                , jobtype NVARCHAR(1024)
                , jobtypeNoVersion NVARCHAR(1024)
                , datalengthNA INT
                , module_id INT
                , level_id INT
                , datafeed_id INT
                , datafeed_history_id INT
                , data_publication_id INT
                , campaign_id XML
                , notification_template_id INT
                , field_id VARCHAR(MAX)
                , content_id VARCHAR(MAX)
                , field_id_count INT
                , content_id_count INT
                , generation INT
                , root_job_id UNIQUEIDENTIFIER
                , root_JobType NVARCHAR(1023)
                , last_EnqueueTime DATETIME
                , last_process_id INT
                , last_endpoint NVARCHAR(1024)
                ,  last_StartTime DATETIME
                ,  last_EndTime DATETIME
                ,  last_durationM DECIMAL(10,3)
                ,  instrumentation_count INT
                ,  max_async_instrumentation_id BIGINT
                ,  instrumentation_details XML
                , last_touch_time DATETIME
            )
            """, """
                INSERT INTO #jobDetail
                    ( jobid
                    , instrumentation_count
                    , max_async_instrumentation_id
                    , last_touch_time
                    , datalengthNA)
                    SELECT ai.JobId, COUNT(*), MAX(ai.async_instrumentation_id), COALESCE(MAX(ai.EndTime),MAX(ai.StartTime),MAX(ai.InactiveUntil),MAX(ai.EnqueueTime)) last_touch_time
                    , MAX(DATALENGTH(ai.named_arguments))
                    FROM dbo.tblAsyncInstrumentation ai WITH (NOLOCK)
                    LEFT JOIN dbo.tblAsyncJobQueue ajq WITH (NOLOCK) ON ajq.JobId = ai.JobId
                    GROUP BY ai.jobid
                    ORDER BY COALESCE(MAX(ai.EndTime),MAX(ai.StartTime),MAX(ai.InactiveUntil),MAX(ai.EnqueueTime)) DESC
            """, """
                UPDATE jd
                SET jd.jobtype =  ai.JobType
                ,jd.jobtypeNoVersion = SUBSTRING(ai.JobType,12,PATINDEX('%, version=%',ai.JobType)-12)
                , jd.root_job_id = CASE WHEN ai.root_job_id <> ai.JobId THEN ai.root_job_id ELSE NULL  /*'00000000-0000-0000-0000-000000000000'*/  END
                , jd.generation = ai.generation
                , jd.last_EnqueueTime = ai.EnqueueTime
                , jd.last_process_id = ai.process_id
                , jd.last_endpoint = ai.EngineInstance
                , jd.last_StartTime = ai.StartTime
                , jd.last_EndTime = ai.EndTime
                , jd.last_DurationM = DATEDIFF(SECOND, ai.StartTime, ai.EndTime)/60.0
                --, jd.datalengthNA = DATALENGTH(ai.named_arguments)
                FROM #jobDetail jd
                JOIN dbo.tblAsyncInstrumentation ai WITH (NOLOCK)  ON ai.JobId = jd.jobid AND ai.async_instrumentation_id = jd.max_async_instrumentation_id
            """, """
                WITH XMLNAMESPACES ('http://schemas.microsoft.com/2003/10/Serialization/Arrays' AS a, 'http://schemas.datacontract.org/2004/07/System.Collections.Generic' AS b, 'http://schemas.microsoft.com/2003/10/Serialization/' AS z)
                UPDATE jd
                SET level_id =
                CASE WHEN ajq.JobType LIKE 'ArcherTech.JobPackages.CalculationService.ScheduleRecalculateWorkflow, ArcherTech.JobPackages.CalculationService%'
                OR ajq.JobType LIKE 'ArcherTech.JobPackages.CalculationService.ScheduleRecalculateWorkflow, ArcherTech.JobPackages.CalculationService%'
                OR ajq.JobType LIKE 'ArcherTech.JobPackages.CalculationService.PhysicalCalculationsWorkflow, ArcherTech.JobPackages.CalculationService%'
                THEN  ajq.named_arguments.value('(a:ArrayOfKeyValueOfstringanyType/KeyValuePairs/b:KeyValuePairOfstringanyType/b:value)[1]','int')
                    END
                , datafeed_id   =
                CASE WHEN ajq.JobType LIKE 'ArcherTech.DataFeed.Workflows.DirectExecuteDataFeedWorkflow, ArcherTech.DataFeed%'
                OR ajq.JobType LIKE 'ArcherTech.DataFeed.Workflows.ScheduledDataFeedWorkflow, ArcherTech.DataFeed%'
                THEN
                ajq.named_arguments.value('(a:ArrayOfKeyValueOfstringanyType/KeyValuePairs/b:KeyValuePairOfstringanyType/b:value)[1]','int')
                END
                , datafeed_history_id =
                CASE WHEN ajq.JobType LIKE 'ArcherTech.DataFeed.Workflows.ExecuteDataFeedWorkflow, ArcherTech.DataFeed%' THEN
                ajq.named_arguments.value('(a:ArrayOfKeyValueOfstringanyType/KeyValuePairs/b:KeyValuePairOfstringanyType/b:value)[1]','int')
                    END
                , data_publication_id =
                CASE WHEN ajq.JobType LIKE 'ArcherTech.DataPublication.Workflow.DataPublicationWorkflow, ArcherTech.DataPublication%' THEN
                ajq.named_arguments.value('(a:ArrayOfKeyValueOfstringanyType/KeyValuePairs/b:KeyValuePairOfstringanyType/b:value)[1]','int')
                    END
                , notification_template_id =
                CASE WHEN ajq.JobType LIKE 'ArcherTech.Notifications.Workflow.SendNotification.SendNotificationJob, ArcherTech.Notifications%' THEN
                ajq.named_arguments.value('(a:ArrayOfKeyValueOfstringanyType/KeyValuePairs/b:KeyValuePairOfstringanyType/b:value)[1]','int')
                    END
                , field_id =
                CASE WHEN ajq.jobtype LIKE 'ArcherTech.Kernel.Jobs.ScoreCardCalculationContentScopeJobHandler, ArcherTech.Kernel.Jobs%' THEN
                '<int>'+CAST(ajq.named_arguments.value('(a:ArrayOfKeyValueOfstringanyType/KeyValuePairs/b:KeyValuePairOfstringanyType/b:value)[1]','int') AS VARCHAR(20))+'</int>'
                END
                , content_id =
                CASE WHEN ajq.jobtype LIKE 'ArcherTech.Kernel.Jobs.ScoreCardCalculationContentScopeJobHandler, ArcherTech.Kernel.Jobs%' THEN
                '<int>'+CAST(ajq.named_arguments.value('(a:ArrayOfKeyValueOfstringanyType/KeyValuePairs/b:KeyValuePairOfstringanyType/b:value)[2]','int') AS VARCHAR(20))+'</int>'
                END
                FROM #jobDetail jd
                JOIN dbo.tblAsyncInstrumentation ajq WITH (NOLOCK) ON ajq.JobId = jd.jobid
                WHERE ajq.named_arguments IS NOT NULL;
            """, """
                UPDATE jd
                SET jd.datafeed_id = dfh.datafeed_id
                FROM #jobDetail jd
                JOIN dbo.tblDataFeedHistory dfh WITH (NOLOCK) ON dfh.datafeed_history_id = jd.datafeed_history_id
            """, """
                UPDATE jd
                SET jd.level_id = nt.level_id
                FROM #jobDetail jd
                JOIN dbo.tblNotificationTemplate nt WITH (NOLOCK) ON nt.notification_template_id = jd.notification_template_id
            """, """
                UPDATE jd
                SET jd.level_id = d.level_id
                FROM #jobDetail jd
                JOIN dbo.tblDatafeed d WITH (NOLOCK) ON d.datafeed_id = jd.datafeed_id
                JOIN tblLevel l WITH (NOLOCK) ON l.level_id = d.level_id
            """, """
                UPDATE cj SET cj.root_JobType = ai.JobType
                FROM #jobDetail cj
                JOIN dbo.tblAsyncInstrumentation ai WITH (NOLOCK)  ON ai.JobId = cj.root_job_id
            """, """
                UPDATE jd
                SET
                instrumentation_details = CAST((SELECT
                ajq.async_instrumentation_id [@async_instrumentation_id]
                , ajq.EnqueueTime [@EnqueueTime]
                ,ajq.StartTime [@StartTime]
                , ajq.EndTime [@EndTime]
                , DATEDIFF(SECOND,ajq.StartTime, ajq.EndTime )/60.0 [@durationM]
                ,ajq.EngineInstance [@EngineInstance]
                ,ajq.process_id [@process_id]
                ,ajq.Reason [@Reason]
                FROM dbo.tblAsyncInstrumentation ajq
                WHERE ajq.JobId = ai.jobid
                FOR XML PATH ('V')
                ) AS XML)
                FROM dbo.tblAsyncInstrumentation ai WITH (NOLOCK)
                JOIN #jobDetail jd ON ai.JobId = jd.jobid
            """
        ],
        "select":
        "SELECT * FROM #jobDetail jd",
        "columns": [
            "jobid", "jobtype", "jobtypeNoVersion", "datalengthNA",
            "module_id", "level_id", "datafeed_id", "datafeed_history_id",
            "data_publication_id", "campaign_id", "notification_template_id",
            "field_id", "content_id", "field_id_count", "content_id_count",
            "generation", "root_job_id", "root_JobType", "last_EnqueueTime",
            "last_process_id", "last_endpoint", "last_StartTime",
            "last_EndTime", "last_durationM", "instrumentation_count",
            "max_async_instrumentation_id", "instrumentation_details",
            "last_touch_time"
        ]
    },
    "calculations": {
        "configure": [],
        "select": []
    },
    "campaign": {
        "configure": [],
        "select": []
    }
}
