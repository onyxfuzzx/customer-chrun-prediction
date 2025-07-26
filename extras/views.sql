Create View vw_ChurnData as
    select * from prod_Churn where Churn In ('Yes', 'No')