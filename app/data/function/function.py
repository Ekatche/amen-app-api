from django.db import connection


def make_query(query):
    """ """
    with connection.cursor() as cursor:
        cursor.execute(query)
        list_elem = cursor.fetchall()
        list_column = cursor.description
    list_result_as_dict = [
        {column.name: value for column, value in zip(list_column, row)}
        for row in list_elem
    ]
    return list_result_as_dict


def get_global_data_per_month():
    """
    get stats about sales
    """

    sql_query = """SELECT
        o.date_created::DATE as date,
        COUNT(o.id) as total_order,
        SUM(oi.quantity) as total_quantity_sold,
        ROUND(AVG(pd.price), 2) as avg_order_amount,
        SUM(o.amount_due) as revenue
        FROM order_order o
        JOIN order_orderitem oi ON oi.order_id = o.id
        JOIN products_product pd ON oi.product_id = pd.id
        GROUP BY o.date_created::DATE
        ORDER BY o.date_created::DATE ASC
    """
    result = make_query(sql_query)

    return result


def products_sold():
    sql_query = """SELECT
        SUM(oi.quantity) as total_quantity_sold
        FROM order_order o
        JOIN order_orderitem oi ON oi.order_id = o.id
        JOIN products_product pd ON oi.product_id = pd.id
    """
    result = make_query(sql_query)
    return result


def total_revenue():
    sql_query = """SELECT
        SUM(o.amount_due) as revenue
        FROM order_order o
        JOIN order_orderitem oi ON oi.order_id = o.id
        JOIN products_product pd ON oi.product_id = pd.id
    """
    result = make_query(sql_query)
    return result


def number_of_clients():
    """
    count the users that have at least one order
    """
    sql_query = """select count(customer_id) as clients
    FROM order_order o
    JOIN core_user u on o.customer_id = u.id
    """
    result = make_query(sql_query)
    return result


def make_query_product():
    sql_query = """SELECT
    EXTRACT(year from o.date_created) as year,
    EXTRACT(month from o.date_created) as month,
    pd.name,
    SUM(quantity) as quantity_sold,
    (price * SUM(quantity))as total_revenue
    from
    order_orderitem oi
    JOIN order_order o on oi.order_id=o.id
    JOIN products_product pd on pd.id = oi.product_id
    GROUP BY pd.name, pd.id, EXTRACT(year from o.date_created),
    EXTRACT(month from o.date_created)
    """
    result = make_query(sql_query)
    return result
