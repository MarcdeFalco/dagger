# dagger
A semantic-based website to publish mathematics, based upon a Directed Acyclic Graph of knowledge

# Installation
Clone, then run in a virtualenv

    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver

in order to fetch every needed package, create the database and run the development server.

# Editing

To start editing you have to add a superuser account:

    python manage.py createsuperuser

Then you can log into the admin interface from the top navbar.

To enter content you'll have to:

* Add Atom types for each different type of atoms (Theorem, Lemma, ...). 
The important flag specify which atoms get to be displayed in the dag by default.
The bootstrap theme is one of default, primary, success, info or warning and it changes the color of the corresponding atoms.
* Add Atom relationship types (needs, apply, ...)
* Add Atoms by using textile markup. To make a link to another atom:


        "link text":relationslug:atomref

 The atom ref can be the slug of the target atom or it's id.
* Then you can add handout compounded from different atoms. The handout format is given in the admin form. You can directly define atoms inside handouts, they'll get created on save.
Here is an example of an handout code:

         Title of the handout
         * First paragraph
         ** First subparagraph
         -{ definition inlineatom
          This is an inlined atom definition.
         }
         This text will be placed before the atom
         --
         And this text will be placed after
         - insert_an_existing_atom
       