from configs.database import DB
from bson.objectid import ObjectId
from typing import Union
from threading import Thread

"""
How to use the DB object directly
-------------------------------
Process 1:
    from configs.database import DB
    db   = DB()
    data = db.accounts.find({"name":"Jhon"})

Process e:
    from models.models BaseModel
    DB   = BaseModel('accounts')
    data = DB.collection.find({"name":"Jhon"})
"""

class BaseModel:
    db = ''
    collection = ''

    def __init__(self, collection_name):
        self.db = DB()
        self.collection = self.db[collection_name]

    def count(self, filter: dict = {}) -> int:
        """
        Count the number of documents in the collection that
        match the given filter.

        Parameters:
            filter (dict): The filter to apply to the documents.
            Optional. Defaults to an empty dictionary.

        Returns:
            int: The number of documents that match the filter.
        """
        return self.collection.count_documents(filter)

    def distinct(self, field: str) -> list:
        """
        Get distinct values of a specified field in the collection.

        Parameters:
            field (str): The field to get distinct values of.

        Returns:
            list: A list of distinct values of the specified field.
        """
        return self.collection.distinct(field)

    def find_by_id(self, _id: str):
        """
        Find a document in the collection by its ID.

        Parameters:
            _id (str): The ID of the document to find.

        Returns:
            dict or None: The document with the given ID, or None if no document is found.
        """
        return self.collection.find_one({"_id": ObjectId(_id)})

    def update_by_id(self, _id: str, update_data: dict) -> int:
        """
        Updates a document in the collection by its ID.

        Parameters:
            _id (str): The ID of the document to update.
            update_data (dict): The data to update the document with.

        Returns:
            int: The number of documents modified.
        """
        return self.collection.update_one({"_id": ObjectId(_id)}, {'$set': update_data}).modified_count

    def delete_by_id(self, _id: str) -> int:
        """
        Deletes a document from the collection by its ID.

        Parameters:
            _id (str): The ID of the document to delete.

        Returns:
            int: The number of documents deleted.
        """
        return self.collection.delete_one({"_id": ObjectId(_id)}).deleted_count

    def insert(self, data: Union[dict, list]) -> Union[list,None]:
        """
        Inserts data into the collection.

        This function takes in either a single dictionary or a list of dictionaries
        and inserts them into the collection. It returns a list of inserted IDs.

        Parameters:
            data (Union[dict, list]): The data to be inserted.
            It can be a single dictionary or a list of dictionaries.

        Returns:
            list[ObjectId] or None: returns a list of inserted IDs as ObjectIds
            or None if data is not a dictionary or list of dictionaries.
        """
        if type(data) == dict:
            # Check if the data is a single dictionary
            # Insert the dictionary into the collection and return the inserted ID
            return [self.collection.insert_one(data).inserted_id]
        elif type(data) == list:
            # Check if the data is a list of dictionaries
            # Insert the list of dictionaries into the collection and return the inserted IDs
            return self.collection.insert_many(data).inserted_ids
        else:
            # If the data is neither a dictionary nor a list of dictionaries, return None
            return None

    def update(self, filter: dict, update_data: dict, update_all: bool = True) -> int:
        """
        Updates a document in the collection based on the filter.

        Parameters:
            filter (dict): The filter to select the document(s) to be updated.
            update_data (dict): The data to be updated.
            update_all (bool): If True, updates all documents matching the filter.
                If False, updates only the first document matching the filter.
                Defaults to False.

        Returns:
            int: The number of documents modified.
        """
        if update_all:
            # If 'update_all' is True, use 'update_many' to update all documents
            # matching the filter. The '$set' operator is used to update the
            # fields specified in 'update_data'.
            return self.collection.update_many(filter, {'$set': update_data}).modified_count
        else:
            # If 'update_all' is False, use 'update_one' to update only the first
            # document matching the filter. The '$set' operator is used to update
            # the fields specified in 'update_data'. It follows the default sorting
            # order of Mongo, i.e. latest first.
            return self.collection.update_one(filter, {'$set': update_data}).modified_count

    def delete(self, filter: dict) -> int:
        """
        Deletes all matching documents from the collection based on the given filter.

        Parameters:
            filter (dict): The filter to select the documents to be deleted.

        Returns:
            int: The number of documents deleted.
        """
        return self.collection.delete_many(filter).deleted_count

    def find_one(self, filter: dict):
        """
        Finds a single document in the collection that matches the given filter.

        Args:
            filter (dict): A dictionary specifying the query criteria for the document.

        Returns:
            Optional[dict]: The first document that matches the filter, or None if no document is found.
        """
        return self.collection.find_one(filter)

    def find_all(self, filter: dict={}, skip: int=0, limit: int=0) -> list:
        """
        Retrieves all documents from the collection that match the given filter.

        Args:
            filter (dict, optional): A dictionary representing the query filter.
            Defaults to an empty dictionary.

            skip (int, optional): The number of documents to skip. Defaults to 0.

            limit (int, optional): The maximum number of documents to return.
            Defaults to 0.

        Returns:
            list: A list of dictionaries representing the documents that match
            the filter. Each dictionary contains the document data with an
            additional '_id' field containing the document's ObjectId as a string.
        """
        data = self.collection.find(filter)
        if limit > 0:
            data = data.limit(limit)
        if skip > 0:
            data = data.skip(skip)

        return [{**field, '_id': str(field['_id'])} for field in data]

    def insert_on_thread(self, insert_data: dict) -> None:
        """
        Insert the given data into the collection on a separate thread
        without blocking the main thread and without waiting for the result.

        Args:
            insert_data (dict): The data to be inserted into the collection.

        Returns:
            None
        """
        thread = Thread(target=self.insert, args=(insert_data,))
        thread.start()

    def update_on_thread(self, filter: dict, update_data: dict, update_all: bool = True) -> None:
        """
        Update the documents in the collection that match the given filter on a separate thread
        without blocking the main thread and without waiting for the result.

        Args:
            filter (dict): A dictionary representing the query filter.

            update_data (dict): A dictionary representing the update to be applied to the matching documents.

            update_all (bool, optional): If True, update all matching documents. If False, update only the first matching document.
            Defaults to True.

        Returns:
            None
        """
        thread = Thread(target=self.update, args=(filter, update_data, update_all,))
        thread.start()

    def delete_on_thread(self, filter: dict) -> None:
        """
        Delete the documents in the collection that match the given filter on a separate thread
        without blocking the main thread and without waiting for the result.

        Args:
            filter (dict): A dictionary representing the query filter.

        Returns:
            None
        """
        thread = Thread(target=self.delete, args=(filter,))
        thread.start()
