from request_validation import BaseValidator, RequestParamError, add_into_dtype_map


@add_into_dtype_map
class CommaStringListValidator(BaseValidator):
    dtype = "commalist"

    def _validate(self, data):
        if self.dtype is not str:
            raise RequestParamError(f"{self._log_prefix} need to be string")
        data = data.split(",")
        return data


def main():
    return

if __name__ == "__main__":
    main()
