-- Cases_Dimension Table
CREATE TABLE IF NOT EXISTS Cases_Dimension (
    Cases_ID UUID NOT NULL PRIMARY KEY,
    Last_Update_ET TIMESTAMP,
    State_Number INT
);

-- Cases Fact Table
CREATE TABLE IF NOT EXISTS Cases_Fact (
    Cases_ID UUID NOT NULL REFERENCES Cases_Dimension(Cases_ID),
    Total_Cases INT,
    Population_Percent FLOAT,
    New_Cases INT,
    Seven_Day_Change_Percent FLOAT
);

-- Testing Fact Table
CREATE TABLE IF NOT EXISTS Testing_Fact (
    Cases_ID UUID NOT NULL REFERENCES Cases_Dimension(Cases_ID),
    Total_Tests INT,
    Population_Percent FLOAT,
    New_Tests INT,
    Seven_Day_Change_Percent FLOAT
);

-- Hospitalization Fact Table
CREATE TABLE IF NOT EXISTS Hospitalization_Fact (
    Cases_ID UUID NOT NULL REFERENCES Cases_Dimension(Cases_ID),
    Currently_Hospitalized INT,
    Population_Percent_Hospitalized FLOAT,
    Change_in_Hospitalized INT,
    Seven_Day_Change_Percent_Hospitalized FLOAT,
    Seven_Day_Change_Avg_Hospitalized FLOAT,
    Currently_in_ICU INT,
    Population_Percent_ICU FLOAT,
    Change_in_ICU INT,
    Seven_Day_Change_Percent_ICU FLOAT,
    Seven_Day_Change_Avg_ICU FLOAT,
    Currently_on_Ventilator INT,
    Population_Percent_Ventilator FLOAT,
    Change_in_Ventilator INT,
    Seven_Day_Change_Percent_Ventilator FLOAT,
    Seven_Day_Change_Avg_Ventilator FLOAT
);

-- Death Fact Table
CREATE TABLE IF NOT EXISTS Death_Fact (
    Cases_ID UUID NOT NULL REFERENCES Cases_Dimension(Cases_ID),
    Total_Deaths INT,
    Population_Percent FLOAT,
    New_Deaths INT,
    Seven_Day_Change_Percent FLOAT,
    Seven_Day_Change_Avg FLOAT
);

-- Field Definitions Dimension Table
CREATE TABLE IF NOT EXISTS Field_Definitions_Dimension (
    Field_Definitions_Dimension_ID UUID NOT NULL PRIMARY KEY,
    Field_Name VARCHAR(100) ,
    Field_Path VARCHAR(100),
    Deprecated BOOLEAN,
    Prior_Names VARCHAR(100)
);
