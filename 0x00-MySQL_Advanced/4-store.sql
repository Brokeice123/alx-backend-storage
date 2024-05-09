-- Script that creates a trigger that decreases
-- the quantity of an item after adding a new order

DELIMITER //
CREATE TRIGGER decrease_quantity_after_order_creation AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END //

DELIMITER ;