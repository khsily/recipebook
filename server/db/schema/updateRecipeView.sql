UPDATE recipe 
   SET view = view + 1
WHERE id = %(id)s;