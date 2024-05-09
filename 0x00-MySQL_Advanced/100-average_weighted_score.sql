DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
  UPDATE users 
  SET average_weighted_score = (
    SELECT AVG(score * projects.weight)
    FROM corrections
    JOIN projects ON projects.id = corrections.project_id
    WHERE corrections.user_id = user_id
  )
  WHERE id = user_id;
END//
DELIMITER ;
