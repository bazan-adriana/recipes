from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import user_model


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.descriptions = data['descriptions']
        self.instructions = data['instructions']
        self.date = data['date']
        self.under30 = data['under30']
        self.user_id = data['user_id']


#  =============    CREATE    ============
    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO recipes (name, descriptions, instructions, date, under30, user_id)
            VALUES (%(name)s,%(descriptions)s,%(instructions)s,%(date)s,%(under30)s,%(user_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)


#  ===========  READ ALL  =============
    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM recipes
                JOIN users
                ON recipes.user_id = users.id;
            """
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        all_recipes = []
        if results:
            for row in results:
                # create each recipe
                this_recipe = cls(row)       # instantiate a recipe
            # create the user for this recipe
                user_data = {                # prepare the dict for the user constructor
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'],
                    **row
                }
# now we can make a user
                this_user = user_model.User(user_data)
            # add new attribute
                this_recipe.planner = this_user
                all_recipes.append(this_recipe)
        return all_recipes


#  ============    READ ONE   ==================
    @classmethod
    def get_by_id(cls, data):
        query = """
            SELECT * FROM recipes
            JOIN users
            ON recipes.user_id = users.id
            WHERE recipes.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        if results:
            # init the recipe
            this_recipe = cls(results[0])
# init the user and attach the recipe
            row = results[0]
            user_data = {
                **row,
                'id': row['users.id'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            # create a User obj here
            this_user = user_model.User(user_data)
            this_recipe.planner = this_user    # adding a new attribute to the recipe
            return this_recipe
        return False


#  ===============    UPDATE   ==================
    @classmethod
    def update(cls, data):
        query = """
            UPDATE recipes
            SET
            name = %(name)s,
            descriptions = %(descriptions)s,
            instructions = %(instructions)s,
            date = %(date)s,
            under30 = %(under30)s
            WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)


#  ===============    DELETE   ===========================
    @classmethod
    def delete(cls, data):
        query = """
        DELETE FROM recipes
        Where id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)




#  ===================  VALIDATOR  =========================
    @staticmethod
    def validator(form_data):
        is_valid = True

        if len(form_data['name']) < 1:
            is_valid = False
            flash("Name must not be blank", 'form_validate')

        if len(form_data['descriptions']) < 1:
            is_valid = False
            flash("Description must not be blank", 'form_validate')

        if len(form_data['instructions']) < 1:
            is_valid = False
            flash("Instructions must not be blank", 'form_validate')

        if len(form_data['date']) < 1:
            is_valid = False
            flash("Date must not be blank", 'form_validate')

        if 'under30' not in form_data:
            is_valid = False
            flash("Under 30 minutes? must not be blank", 'form_validate')

        return is_valid



