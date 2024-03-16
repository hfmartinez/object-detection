queries = {
    "INSERT_IMG": """
        insert into images  (name, obj_id) values ('{name}', {obj_id});
    """,
    "INSERT_OBJ": """
        insert into objects  (x, y, w, h, label) values ({x}, {y}, {w}, {h}, '{label}') RETURNING id;
    """,
}
