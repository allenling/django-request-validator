
**still extracting and checking values from request.query_param or request.data like this?**


.. code-block:: python

    from rest_framework.views import APIView
    class MyView(APIView):

        def post(self, request):
            a = request.query_param.get("a", None)
            if a is None:
                # do sth
                pass
            if type(a) is not int:
                # do sth
                pass
            data = {"a": a}
            return Response(data)


**but actually you could do extracting and checking like this**

.. code-block:: python

    from rest_framework.views import APIView
    from request_validation import add_query_param_validator, add_data_validator, create_validator_func
    class RequestValidatorView(APIView):

        @add_data_validator("q", allow_none=True, default=10, dtype="int")
        @add_data_validator("p", allow_none=True, dtype="string")
        @add_data_validator("n", default=1, dtype="int")
        @add_data_validator("m", dtype="list")
        @add_query_param_validator("k", dtype="float")
        @add_query_param_validator("z", dtype="commalist")
        @add_query_param_validator("y", dtype="string")
        @add_query_param_validator("x", dtype="int")
        @create_validator_func
        def post(self, request, a, x, y, z, k, m, n, p, q):
            # a came from URL
            # x, y and z came from request.query_param
            # m, n, p, q came from request.data
            # if request.data did not contain key n, n would be 1, but we do not allow request.data[n] to be None
            # we allow request.data[p] to be None, but would raise a Exception if request.data did not contain key p
            # for q, both would work
            data = {"a": a, "x": x, "y": y, "z": z, "k": k, "m": m, "n": n, "p": p, "q": q}
            return Response(data)

and you can easy to figure out how many params or data your views would need, and what type of them should be

if the type of the value that we got from the front-end, or anywhere, mismatched the configured type, we would raise a exception

how to handle this exception(request_validation.RequestParamError) is on you