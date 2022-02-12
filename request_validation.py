
class RequestParamError(Exception):
    pass


DTYPE_MAP = {}


def add_into_dtype_map(cls):
    DTYPE_MAP[cls.dtype] = cls
    return cls


class BaseValidator:

    def __init__(self, pos, key, allow_none=False, default=None):
        assert pos == "query_params" or pos == "data"
        self.pos = pos
        self.key = key
        self.allow_none = allow_none
        self.default = default
        self._log_prefix = f"request.{self.pos}[{self.key}]"
        return

    def validate(self, req):
        req_attr = getattr(req, self.pos)
        if self.key not in req_attr:
            if self.default:
                return self.default
            raise RequestParamError(f"{self._log_prefix} does not exist")
        data = req_attr[self.key]
        if data is None:
            if self.allow_none:
                return None
            else:
                raise RequestParamError(f"{self._log_prefix} can not be None")
        self.dtype = type(data)
        data = self._validate(data)
        return data

    def _validate(self, data):
        raise NotImplementedError


# ===============================================================


@add_into_dtype_map
class StringValidator(BaseValidator):
    dtype = "string"

    def _validate(self, data):
        if self.dtype is not str:
            data = str(data)
        return data


@add_into_dtype_map
class ListValidator(BaseValidator):
    dtype = "list"

    def _validate(self, data):
        if self.dtype is not list:
            raise RequestParamError(f"{self._log_prefix} need to be list")
        return data


@add_into_dtype_map
class IntValidator(BaseValidator):
    dtype = "int"

    def _validate(self, data):
        if self.dtype is not int and self.dtype is not str:
            raise RequestParamError(f"{self._log_prefix} need to be float/int")
        try:
            data = int(data)
        except Exception as e:
            raise RequestParamError(f"{self._log_prefix} can not be transformed to int")
        return data


@add_into_dtype_map
class FloatValidator(BaseValidator):
    dtype = "float"

    def _validate(self, data):
        if self.dtype is not float and self.dtype is not str:
            raise RequestParamError(f"{self._log_prefix} need to be float/str")
        try:
            data = float(data)
        except Exception as e:
            raise RequestParamError(f"{self._log_prefix} can not be transformed to float")
        return data


# =====================================================================


def create_validator_func(view_func):
    def validator_func(self, request, *args, **kwargs):
        datas = {}
        for i in validator_func.__validate_keys__:
            v = i.validate(request)
            datas[i.key] = v
        datas.update(kwargs)
        return view_func(self, request, **datas)
    validator_func.__validate_keys__ = []
    return validator_func


def add_query_param_validator(key, allow_none=False, default=None, validator_class=None, dtype=None):
    def add_param_into_validator(validator_func):
        _validator_class = validator_class
        if _validator_class is None and dtype is None:
            raise KeyError(f"{key} validator_class is None")
        elif _validator_class is None:
            _validator_class = DTYPE_MAP.get(dtype, None)
            if _validator_class is None:
                raise KeyError(f"{key} validator_class is None")
        key_obj = _validator_class("query_params", key, allow_none=allow_none, default=default)
        validator_func.__validate_keys__.append(key_obj)
        return validator_func
    return add_param_into_validator


def add_data_validator(key, allow_none=False, default=None, validator_class=None, dtype=None):
    def add_data_into_validator(validator_func):
        _validator_class = validator_class
        if _validator_class is None and dtype is None:
            raise KeyError(f"{key} validator_class is None")
        elif _validator_class is None:
            _validator_class = DTYPE_MAP.get(dtype, None)
            if _validator_class is None:
                raise KeyError(f"{key} validator_class is None")
        key_obj = _validator_class("data", key, allow_none=allow_none, default=default)
        validator_func.__validate_keys__.append(key_obj)
        return validator_func
    return add_data_into_validator


def main():
    return

if __name__ == "__main__":
    main()
