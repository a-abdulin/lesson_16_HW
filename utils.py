import json


def read_json(file_name):
    with open(file_name, 'r', encoding = "utf-8") as file:
        file_data = json.load(file)
    return file_data


def users_instance_to_dict(instance):
    return {
        "id": instance.id,
        "first_name": instance.first_name,
        "last_name": instance.last_name,
        "age": instance.age,
        "email": instance.email,
        "role": instance.role,
        "phone": instance.phone
    }


def orders_instance_to_dict(instance):
    return {
        "id": instance.id,
        "name": instance.name,
        "description": instance.description,
        "start_date": instance.start_date,
        "end_date": instance.end_date,
        "address": instance.address,
        "price": instance.price,
        "customer_id": instance.customer_id,
        "executor_id": instance.executor_id,
    }


def offers_instance_to_dict(instance):
    return {
        "id": instance.id,
        "order_id": instance.order_id,
        "executor_id": instance.executor_id,
    }

