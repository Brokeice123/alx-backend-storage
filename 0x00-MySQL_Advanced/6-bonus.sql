-- creates a stored procedure AddBonus that adds a new correction for a student

DELIMITER //

DROP PROCEDURE IF EXISTS AddBonus;
CREATE PROCEDURE AddBonus(user_id INT, project_name VARCHAR(255), score INT)
BEGIN
	-- check if project_name exists, if not, create it
	IF NOT EXISTS (SELECT 1 FROM projects WHERE projects.name = project_name) THEN
		INSERT INTO projects (name) VALUES (project_name);
	END IF;
	
	-- get the projects.id value for the newly created project
	SET @project_id = (SELECT projects.id FROM projects WHERE projects.name = project_name);
	
	-- insert the new correction
	INSERT INTO corrections (student_id, project_id, score)
	SELECT users.id, @project_id, score
	FROM users
	WHERE users.id = user_id;
END//
DELIMITER ;
