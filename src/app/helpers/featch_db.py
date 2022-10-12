def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]


def dictfetch(cursor):
    "Returns one row from a cursor as a dict"
    columns = [column[0] for column in cursor.description]
    row = cursor.fetchall()
    if row:
        return dict(zip(columns, row[0]))
    return dict()
