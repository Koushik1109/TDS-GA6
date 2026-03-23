WITH overall AS (
  SELECT AVG(CASE WHEN true_label = predicted_label THEN 1.0 ELSE 0.0 END) AS overall_acc
  FROM predictions
),
slices AS (
  -- Single column slices
  SELECT 
    'platform = ' || platform AS slice_definition,
    COUNT(*) AS slice_size,
    AVG(CASE WHEN true_label = predicted_label THEN 1.0 ELSE 0.0 END) AS slice_accuracy
  FROM predictions
  GROUP BY platform
  HAVING COUNT(*) >= 36
  
  UNION ALL
  
  SELECT 
    'language_detected = ' || language_detected AS slice_definition,
    COUNT(*) AS slice_size,
    AVG(CASE WHEN true_label = predicted_label THEN 1.0 ELSE 0.0 END) AS slice_accuracy
  FROM predictions
  GROUP BY language_detected
  HAVING COUNT(*) >= 36
  
  UNION ALL
  
  SELECT 
    'message_length_bucket = ' || message_length_bucket AS slice_definition,
    COUNT(*) AS slice_size,
    AVG(CASE WHEN true_label = predicted_label THEN 1.0 ELSE 0.0 END) AS slice_accuracy
  FROM predictions
  GROUP BY message_length_bucket
  HAVING COUNT(*) >= 36
  
  -- Two column combinations
  UNION ALL
  
  SELECT 
    'platform = ' || platform || ', language_detected = ' || language_detected AS slice_definition,
    COUNT(*) AS slice_size,
    AVG(CASE WHEN true_label = predicted_label THEN 1.0 ELSE 0.0 END) AS slice_accuracy
  FROM predictions
  GROUP BY platform, language_detected
  HAVING COUNT(*) >= 36
  
  UNION ALL
  
  SELECT 
    'platform = ' || platform || ', message_length_bucket = ' || message_length_bucket AS slice_definition,
    COUNT(*) AS slice_size,
    AVG(CASE WHEN true_label = predicted_label THEN 1.0 ELSE 0.0 END) AS slice_accuracy
  FROM predictions
  GROUP BY platform, message_length_bucket
  HAVING COUNT(*) >= 36
  
  UNION ALL
  
  SELECT 
    'language_detected = ' || language_detected || ', message_length_bucket = ' || message_length_bucket AS slice_definition,
    COUNT(*) AS slice_size,
    AVG(CASE WHEN true_label = predicted_label THEN 1.0 ELSE 0.0 END) AS slice_accuracy
  FROM predictions
  GROUP BY language_detected, message_length_bucket
  HAVING COUNT(*) >= 36
)
SELECT 
  s.slice_definition,
  CAST(s.slice_size AS INTEGER) as slice_size,
  CAST(s.slice_accuracy AS FLOAT) as slice_accuracy,
  CAST(o.overall_acc AS FLOAT) as overall_accuracy
FROM slices s
CROSS JOIN overall o
WHERE s.slice_accuracy <= o.overall_acc - 0.40
ORDER BY s.slice_accuracy ASC
LIMIT 1;
