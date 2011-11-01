Improved F QuerySet Expression
==============================

According to the Django documentation, we know:

Django provides the F() object to allow such comparisons. Instances of F() act as a 
reference to a model field within a query. These references can then be used in query 
filters to compare the values of two different fields on the same model instance.

But the original implementation does not allow the NOT operator on this expression. 
As there is no way to generate a sentence like:

.. code-block:: sql

    UPDATE "niwi_testmodel" SET "done" = NOT "niwi_testmodel"."done";

But on ``django_orm.expressions.F`` implements ~ operator to fill this gap.

Example:
^^^^^^^^

.. code-block:: python

    from django_orm.expressions import F
    from niwi.models import TestModel
    TestModel.objects.update(done=~F('done'))


This generates this sql sentence:

.. code-block:: sql

    UPDATE "niwi_testmodel" SET "done" = NOT "niwi_testmodel"."done";
