 Write a summary of the exploratory data analysis above. What numerical or categorical features were in the data? 

Was there any pattern suggested of a relationship between state and ticket price? 

What did this lead us to decide regarding which features to use in subsequent modeling? 

What aspects of the data (e.g. relationships between features) should you remain wary of when you come to perform feature selection for modeling? 

Two key points that must be addressed are the choice of target feature for your modelling and how, if at all, you're going to handle the states labels in the data.

# Summary of Exploratory Data Analysis 

## Data

The data were comprised of two datasets: Ski Data, and State Summary. The Ski Data file contained the ski resort information for 281 ski resorts in the United States. 

### Ski Resort Data

The Ski Data by category is as follows:

#### Nominal Data 

| Field  | Data Type | Data Class  | Data Category |
| ------ | --------- | ----------- | ------------- |
| Name   | object    | qualitative | nominal       |
| Region | object    | qualitative | nominal       |
| state  | object    | qualitative | nominal       |

#### Ordinal Data 

The number and types of resort transport (e.g, lifts) were treated as ordinal data.

| Field        | Data Type | Data Class   | Data Category |
| ------------ | --------- | ------------ | ------------- |
| trams        | int64     | quantitative | ordinal       |
| fastSixes    | int64     | quantitative | ordinal       |
| fastQuads    | int64     | quantitative | ordinal       |
| quad         | int64     | quantitative | ordinal       |
| triple       | int64     | quantitative | ordinal       |
| double       | int64     | quantitative | ordinal       |
| surface      | int64     | quantitative | ordinal       |
| total_chairs | int64     | quantitative | ordinal       |

#### Continuous Data

Ski area, vertical drop, prices, and other quantitative information were treated as continuous.

| Field             | Data Type | Data Class   | Data Category |
| ----------------- | --------- | ------------ | ------------- |
| summit_elev       | int64     | quantitative | continuous    |
| vertical_drop     | int64     | quantitative | continuous    |
| base_elev         | int64     | quantitative | continuous    |
| Runs              | float64   | quantitative | continuous    |
| TerrainParks      | float64   | quantitative | continuous    |
| LongestRun_mi     | float64   | quantitative | continuous    |
| SkiableTerrain_ac | float64   | quantitative | continuous    |
| Snow              | float64   | quantitative | continuous    |
| daysOpenLastYear  | float64   | quantitative | continuous    |
| yearsOpen         | float64   | quantitative | continuous    |
| averageSnowfall   | float64   | quantitative | continuous    |
| AdultWeekday      | float64   | quantitative | continuous    |
| AdultWeekend      | float64   | quantitative | continuous    |
| projectedDaysOpen | float64   | quantitative | continuous    |
| NightSkiing_ac    | float64   | quantitative | continuous    |

### State Summary Data

State information included relevant state-level information such as the number of resorts per state, total ski area, population statistics, and number of terrain parks. Concretely, the state summary data included:

| Field                       | Data Type | Data Class   | Data Category |
| --------------------------- | --------- | ------------ | ------------- |
| state                       | object    | qualitative  | nominal       |
| resorts_per_state           | int64     | quantitative | continuous    |
| state_total_skiable_area_ac | float64   | quantitative | continuous    |
| state_total_days_open       | float64   | quantitative | continuous    |
| state_total_terrain_parks   | float64   | quantitative | continuous    |
| state_total_nightskiing_ac  | float64   | quantitative | continuous    |
| state_population            | int64     | quantitative | continuous    |
| state_area_sq_miles         | int64     | quantitative | continuous    |

In addition two density measures were derived from the states data.

- Resorts per Capita
- Resorts per Area

All state label data will be included in the model, in addition to the resort density measures.

## Target Variable

The AdultWeekend price was chosen as the target. The majority of visitors and consequently, revenue comes from weekend business.  

## Analysis

The examination began with the state summary dataset. Summary statistics included area, population, days open, resorts, and skiable area by state. The key insights were:

- Montana is among the top 5 largest, but ranked among the least populated states (bottom 6)
- Montana ranks in the top 3rd in terms of the number of resorts by state. New York, Michigan, and Colorado dominate this category with 33, 28, and 22 resorts respectively. Montana currently has 12 ski resorts.
- Montana skiable area ranks 4th among Colorado, Utah, and California.

Resort density measures were created to evaluate the number of resorts vis-a-vis state population and state area.

- Montana ranked among the top 5 states for resorts per capita. Not surprising given Montana's relatively small population.
- Montana ranked in the bottom 3rd of the class for area resort density.

## State-Level Patterns

Prior to visualizing the data, it was scaled and then taken through a process of dimension reduction to reduce the number of dimensions from 7 to 2. The first two components of the Principle Component Analysis accounted for 77% of the variance in data.

Scatterplots of the first two dimensions revealed no state-level patterns in the data. Finally, a heatmap revealed the correlations among all of the predictors. 

## Correlations

### Target Value Correlations

The predictors most highly correlated with the target, AdultWeekend were:

| Field1                          | Correlation |
| ------------------------------- | ----------- |
| Runs                            | 0.756926    |
| fastQuads                       | 0.731445    |
| vertical_drop                   | 0.713287    |
| Snow Making_ac                  | 0.695764    |
| total_chairs                    | 0.654397    |
| daysOpenLastYear                | 0.596674    |
| LongestRun_mi                   | 0.579602    |
| trams                           | 0.569015    |
| projectedDaysOpen               | 0.52965     |
| SkiableTerrain_ac               | 0.52775     |
| fastQuads_runs_ratio            | 0.507635    |
| TerrainParks                    | 0.474914    |
| fastSixes                       | 0.447595    |
| averageSnowfall                 | 0.437216    |
| summit_elev                     | 0.430049    |
| total_chairs_skiable_ratio      | 0.390978    |
| NightSkiing_ac                  | 0.374366    |
| triple                          | 0.346987    |
| total_chairs_runs_ratio         | 0.334912    |
| quad                            | 0.328846    |
| resort_night_skiing_state_ratio | 0.32354     |

Those variables with a correlation above 0.60 are of greatest interest. Next, we examine the multicollinearity among the features.

### Multicollinearity

Here, we have the correlations among the features most highly correlated with the target.

| Field1         | Field2         | Correlation |
| -------------- | -------------- | ----------- |
| Runs           | fastQuads      | 0.720949    |
| total_chairs   | fastQuads      | 0.670023    |
| vertical_drop  | fastQuads      | 0.600392    |
| total_chairs   | Snow Making_ac | 0.583738    |
| Snow Making_ac | fastQuads      | 0.581663    |
| vertical_drop  | Snow Making_ac | 0.550501    |
| vertical_drop  | total_chairs   | 0.396572    |

 The above illuminates issues for the feature selection phase.