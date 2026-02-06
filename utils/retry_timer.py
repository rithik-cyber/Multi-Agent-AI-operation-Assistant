import time
import functools


def retry(max_attempts=3, delay=2):
    """
    Retry decorator for API calls
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    print(f"Retry {attempt + 1}/{max_attempts} failed: {e}")
                    time.sleep(delay)

            raise last_error

        return wrapper

    return decorator


def measure_time(func):
    """
    Measures execution time of a function
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()

        result = func(*args, **kwargs)

        end_time = time.time()
        elapsed_time = round(end_time - start_time, 3)

        return result, elapsed_time

    return wrapper
