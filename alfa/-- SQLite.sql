-- SQLite
SELECT id, quantity, sort_id, multiple_id, parts_id
FROM `alfa_multipleparts`;

DELETE FROM `alfa_multipleparts` WHERE id>0; DELETE FROM `alfa_catalog` WHERE id>26