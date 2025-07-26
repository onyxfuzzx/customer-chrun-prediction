SELECT 
    customerID,
    gender,
    SeniorCitizen,
    Partner,
    Dependents,
    tenure,
    PhoneService,
    MultipleLines,
    InternetService,
    OnlineSecurity,
    OnlineBackup,
    DeviceProtection,
    TechSupport,
    StreamingTV,
    StreamingMovies,
    Contract,
    PaperlessBilling,
    PaymentMethod,
    MonthlyCharges,
    -- Replace NULLs in TotalCharges with string 'None'
    ISNULL(CAST(TotalCharges AS VARCHAR), 'None') AS TotalCharges,
    Churn
INTO [db_churn].[dbo].[prod_Churn]
FROM [db_churn].[dbo].[stg_Churn];
