
--- Gender Wise distribution with percentage --- 
SELECT 
    Gender, 
    COUNT(*) AS TotalCount,
    COUNT(*) * 1.0 / (SELECT COUNT(*) FROM stg_Churn) AS Percentage
FROM 
    stg_Churn
GROUP BY 
    Gender;

--- *** --- *** --- *** --- *** --- *** --- *** ---

--- Contract-wise distribution with percentage ---
SELECT 
    Contract, 
    COUNT(*) AS TotalCount,
    COUNT(*) * 1.0 / (SELECT COUNT(*) FROM stg_Churn) AS Percentage
FROM 
    stg_Churn
GROUP BY 
    Contract;

--- *** --- *** --- *** --- *** --- *** --- *** ---

--- Churn-wise with percentage of Percentage ---

SELECT 
    Churn, 
    COUNT(*) AS TotalCount,
    COUNT(*) * 100.0 / (SELECT COUNT(*) FROM stg_Churn) AS ChurnPercentage
FROM 
    stg_Churn
GROUP BY 
    Churn;


