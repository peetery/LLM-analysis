from typing import TypedDict, List
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result  # for the yield case
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result  # for the yield case
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_yield_from_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = yield from orig(*call_args, **call_kwargs)
        return result  # for the yield case
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = yield from orig(*call_args, **call_kwargs)
        return result  # for the yield case
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = yield from mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = yield from mutants[mutant_name](*call_args, **call_kwargs)
    return result


class Item(TypedDict):
    """
    Represents a single product entry in the order.

    :key name: The name of the product.
    :key price: The price per unit of the product.
    :key quantity: The number of units of the product.
    """
    name: str
    price: float
    quantity: int


class OrderCalculator:
    def xǁOrderCalculatorǁ__init____mutmut_orig(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_1(self, tax_rate=1.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_2(self, tax_rate=0.23, free_shipping_threshold=101.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_3(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=11.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_4(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_5(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError(None)
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_6(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("XXTax rate must be a float or int.XX")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_7(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_8(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("TAX RATE MUST BE A FLOAT OR INT.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_9(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_10(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError(None)
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_11(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("XXFree shipping threshold must be a float or int.XX")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_12(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_13(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("FREE SHIPPING THRESHOLD MUST BE A FLOAT OR INT.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_14(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_15(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError(None)
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_16(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("XXShipping cost must be a float or int.XX")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_17(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_18(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("SHIPPING COST MUST BE A FLOAT OR INT.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_19(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_20(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 1.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_21(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 < tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_22(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate < 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_23(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 2.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_24(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError(None)
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_25(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("XXTax rate must be between 0.0 and 1.0.XX")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_26(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_27(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("TAX RATE MUST BE BETWEEN 0.0 AND 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_28(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold <= 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_29(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 1.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_30(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError(None)
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_31(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("XXFree shipping threshold cannot be negative.XX")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_32(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_33(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("FREE SHIPPING THRESHOLD CANNOT BE NEGATIVE.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_34(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost <= 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_35(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 1.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_36(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError(None)

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_37(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("XXShipping cost cannot be negative.XX")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_38(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_39(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("SHIPPING COST CANNOT BE NEGATIVE.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_40(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = None
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_41(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = None
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_42(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = None
        self.shipping_cost = shipping_cost
    def xǁOrderCalculatorǁ__init____mutmut_43(self, tax_rate=0.23, free_shipping_threshold=100.0, shipping_cost=10.0):
        """
        Initializes a new OrderCalculator instance.
        Initializes an empty list of items (each represented as a TypedDict 'Item')
        and stores the configured tax and shipping parameters.

        :param tax_rate: The percentage of tax applied to the final amount, expressed as a float between 0.0 and 1.0 (default is 0.23 for 23%).
        :param free_shipping_threshold: The minimum order value (after discount) that qualifies for free shipping (default is 100.0).
        :param shipping_cost: The cost of shipping applied if the order does not meet the free shipping threshold (default is 10.0).

        :raises ValueError:
            - If tax_rate is not in the range [0.0, 1.0].
            - If free_shipping_threshold is negative.
            - If shipping_cost is negative.
        :raises TypeError: If any parameter is of incorrect type.
        """
        if not isinstance(tax_rate, (float, int)):
            raise TypeError("Tax rate must be a float or int.")
        if not isinstance(free_shipping_threshold, (float, int)):
            raise TypeError("Free shipping threshold must be a float or int.")
        if not isinstance(shipping_cost, (float, int)):
            raise TypeError("Shipping cost must be a float or int.")
        if not 0.0 <= tax_rate <= 1.0:
            raise ValueError("Tax rate must be between 0.0 and 1.0.")
        if free_shipping_threshold < 0.0:
            raise ValueError("Free shipping threshold cannot be negative.")
        if shipping_cost < 0.0:
            raise ValueError("Shipping cost cannot be negative.")

        self.items: List[Item] = []
        self.tax_rate = tax_rate
        self.free_shipping_threshold = free_shipping_threshold
        self.shipping_cost = None
    
    xǁOrderCalculatorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOrderCalculatorǁ__init____mutmut_1': xǁOrderCalculatorǁ__init____mutmut_1, 
        'xǁOrderCalculatorǁ__init____mutmut_2': xǁOrderCalculatorǁ__init____mutmut_2, 
        'xǁOrderCalculatorǁ__init____mutmut_3': xǁOrderCalculatorǁ__init____mutmut_3, 
        'xǁOrderCalculatorǁ__init____mutmut_4': xǁOrderCalculatorǁ__init____mutmut_4, 
        'xǁOrderCalculatorǁ__init____mutmut_5': xǁOrderCalculatorǁ__init____mutmut_5, 
        'xǁOrderCalculatorǁ__init____mutmut_6': xǁOrderCalculatorǁ__init____mutmut_6, 
        'xǁOrderCalculatorǁ__init____mutmut_7': xǁOrderCalculatorǁ__init____mutmut_7, 
        'xǁOrderCalculatorǁ__init____mutmut_8': xǁOrderCalculatorǁ__init____mutmut_8, 
        'xǁOrderCalculatorǁ__init____mutmut_9': xǁOrderCalculatorǁ__init____mutmut_9, 
        'xǁOrderCalculatorǁ__init____mutmut_10': xǁOrderCalculatorǁ__init____mutmut_10, 
        'xǁOrderCalculatorǁ__init____mutmut_11': xǁOrderCalculatorǁ__init____mutmut_11, 
        'xǁOrderCalculatorǁ__init____mutmut_12': xǁOrderCalculatorǁ__init____mutmut_12, 
        'xǁOrderCalculatorǁ__init____mutmut_13': xǁOrderCalculatorǁ__init____mutmut_13, 
        'xǁOrderCalculatorǁ__init____mutmut_14': xǁOrderCalculatorǁ__init____mutmut_14, 
        'xǁOrderCalculatorǁ__init____mutmut_15': xǁOrderCalculatorǁ__init____mutmut_15, 
        'xǁOrderCalculatorǁ__init____mutmut_16': xǁOrderCalculatorǁ__init____mutmut_16, 
        'xǁOrderCalculatorǁ__init____mutmut_17': xǁOrderCalculatorǁ__init____mutmut_17, 
        'xǁOrderCalculatorǁ__init____mutmut_18': xǁOrderCalculatorǁ__init____mutmut_18, 
        'xǁOrderCalculatorǁ__init____mutmut_19': xǁOrderCalculatorǁ__init____mutmut_19, 
        'xǁOrderCalculatorǁ__init____mutmut_20': xǁOrderCalculatorǁ__init____mutmut_20, 
        'xǁOrderCalculatorǁ__init____mutmut_21': xǁOrderCalculatorǁ__init____mutmut_21, 
        'xǁOrderCalculatorǁ__init____mutmut_22': xǁOrderCalculatorǁ__init____mutmut_22, 
        'xǁOrderCalculatorǁ__init____mutmut_23': xǁOrderCalculatorǁ__init____mutmut_23, 
        'xǁOrderCalculatorǁ__init____mutmut_24': xǁOrderCalculatorǁ__init____mutmut_24, 
        'xǁOrderCalculatorǁ__init____mutmut_25': xǁOrderCalculatorǁ__init____mutmut_25, 
        'xǁOrderCalculatorǁ__init____mutmut_26': xǁOrderCalculatorǁ__init____mutmut_26, 
        'xǁOrderCalculatorǁ__init____mutmut_27': xǁOrderCalculatorǁ__init____mutmut_27, 
        'xǁOrderCalculatorǁ__init____mutmut_28': xǁOrderCalculatorǁ__init____mutmut_28, 
        'xǁOrderCalculatorǁ__init____mutmut_29': xǁOrderCalculatorǁ__init____mutmut_29, 
        'xǁOrderCalculatorǁ__init____mutmut_30': xǁOrderCalculatorǁ__init____mutmut_30, 
        'xǁOrderCalculatorǁ__init____mutmut_31': xǁOrderCalculatorǁ__init____mutmut_31, 
        'xǁOrderCalculatorǁ__init____mutmut_32': xǁOrderCalculatorǁ__init____mutmut_32, 
        'xǁOrderCalculatorǁ__init____mutmut_33': xǁOrderCalculatorǁ__init____mutmut_33, 
        'xǁOrderCalculatorǁ__init____mutmut_34': xǁOrderCalculatorǁ__init____mutmut_34, 
        'xǁOrderCalculatorǁ__init____mutmut_35': xǁOrderCalculatorǁ__init____mutmut_35, 
        'xǁOrderCalculatorǁ__init____mutmut_36': xǁOrderCalculatorǁ__init____mutmut_36, 
        'xǁOrderCalculatorǁ__init____mutmut_37': xǁOrderCalculatorǁ__init____mutmut_37, 
        'xǁOrderCalculatorǁ__init____mutmut_38': xǁOrderCalculatorǁ__init____mutmut_38, 
        'xǁOrderCalculatorǁ__init____mutmut_39': xǁOrderCalculatorǁ__init____mutmut_39, 
        'xǁOrderCalculatorǁ__init____mutmut_40': xǁOrderCalculatorǁ__init____mutmut_40, 
        'xǁOrderCalculatorǁ__init____mutmut_41': xǁOrderCalculatorǁ__init____mutmut_41, 
        'xǁOrderCalculatorǁ__init____mutmut_42': xǁOrderCalculatorǁ__init____mutmut_42, 
        'xǁOrderCalculatorǁ__init____mutmut_43': xǁOrderCalculatorǁ__init____mutmut_43
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOrderCalculatorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁOrderCalculatorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁOrderCalculatorǁ__init____mutmut_orig)
    xǁOrderCalculatorǁ__init____mutmut_orig.__name__ = 'xǁOrderCalculatorǁ__init__'

    def xǁOrderCalculatorǁadd_item__mutmut_orig(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_1(self, name: str, price: float, quantity: int = 2):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_2(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_3(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError(None)
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_4(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("XXItem name must be a string.XX")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_5(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_6(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("ITEM NAME MUST BE A STRING.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_7(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_8(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError(None)
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_9(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("XXPrice must be a number.XX")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_10(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_11(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("PRICE MUST BE A NUMBER.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_12(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_13(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError(None)
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_14(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("XXQuantity must be an integer.XX")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_15(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_16(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("QUANTITY MUST BE AN INTEGER.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_17(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_18(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError(None)
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_19(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("XXItem name cannot be empty.XX")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_20(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_21(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("ITEM NAME CANNOT BE EMPTY.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_22(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity <= 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_23(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 2:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_24(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError(None)
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_25(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("XXQuantity must be at least 1.XX")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_26(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_27(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("QUANTITY MUST BE AT LEAST 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_28(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price < 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_29(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 1:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_30(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError(None)

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_31(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("XXPrice must be greater than 0.XX")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_32(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_33(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("PRICE MUST BE GREATER THAN 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_34(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["XXnameXX"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_35(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["NAME"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_36(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["Name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_37(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] != name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_38(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["XXpriceXX"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_39(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["PRICE"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_40(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["Price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_41(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] == price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_42(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError(None)
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_43(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("XXItem with the same name but different price already exists.XX")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_44(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_45(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("ITEM WITH THE SAME NAME BUT DIFFERENT PRICE ALREADY EXISTS.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_46(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] = quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_47(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["XXquantityXX"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_48(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["QUANTITY"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_49(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["Quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_50(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] -= quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_51(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append(None)

    def xǁOrderCalculatorǁadd_item__mutmut_52(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "XXnameXX": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_53(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "NAME": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_54(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "Name": name,
            "price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_55(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "XXpriceXX": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_56(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "PRICE": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_57(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "Price": price,
            "quantity": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_58(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "XXquantityXX": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_59(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "QUANTITY": quantity
        })

    def xǁOrderCalculatorǁadd_item__mutmut_60(self, name: str, price: float, quantity: int = 1):
        """
        Add an item to the order.

        If an item with the same name and price already exists, its quantity is increased.

        :param name: the name of the item
        :param price: the price of the item
        :param quantity: the quantity of the item (default is 1)
        :raises ValueError: If name is empty, price <= 0, quantity < 1, or item with same name but different price exists.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not isinstance(price, (float, int)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if not name:
            raise ValueError("Item name cannot be empty.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")

        for item in self.items:
            if item["name"] == name:
                if item["price"] != price:
                    raise ValueError("Item with the same name but different price already exists.")
                item["quantity"] += quantity
                return


        self.items.append({
            "name": name,
            "price": price,
            "Quantity": quantity
        })
    
    xǁOrderCalculatorǁadd_item__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOrderCalculatorǁadd_item__mutmut_1': xǁOrderCalculatorǁadd_item__mutmut_1, 
        'xǁOrderCalculatorǁadd_item__mutmut_2': xǁOrderCalculatorǁadd_item__mutmut_2, 
        'xǁOrderCalculatorǁadd_item__mutmut_3': xǁOrderCalculatorǁadd_item__mutmut_3, 
        'xǁOrderCalculatorǁadd_item__mutmut_4': xǁOrderCalculatorǁadd_item__mutmut_4, 
        'xǁOrderCalculatorǁadd_item__mutmut_5': xǁOrderCalculatorǁadd_item__mutmut_5, 
        'xǁOrderCalculatorǁadd_item__mutmut_6': xǁOrderCalculatorǁadd_item__mutmut_6, 
        'xǁOrderCalculatorǁadd_item__mutmut_7': xǁOrderCalculatorǁadd_item__mutmut_7, 
        'xǁOrderCalculatorǁadd_item__mutmut_8': xǁOrderCalculatorǁadd_item__mutmut_8, 
        'xǁOrderCalculatorǁadd_item__mutmut_9': xǁOrderCalculatorǁadd_item__mutmut_9, 
        'xǁOrderCalculatorǁadd_item__mutmut_10': xǁOrderCalculatorǁadd_item__mutmut_10, 
        'xǁOrderCalculatorǁadd_item__mutmut_11': xǁOrderCalculatorǁadd_item__mutmut_11, 
        'xǁOrderCalculatorǁadd_item__mutmut_12': xǁOrderCalculatorǁadd_item__mutmut_12, 
        'xǁOrderCalculatorǁadd_item__mutmut_13': xǁOrderCalculatorǁadd_item__mutmut_13, 
        'xǁOrderCalculatorǁadd_item__mutmut_14': xǁOrderCalculatorǁadd_item__mutmut_14, 
        'xǁOrderCalculatorǁadd_item__mutmut_15': xǁOrderCalculatorǁadd_item__mutmut_15, 
        'xǁOrderCalculatorǁadd_item__mutmut_16': xǁOrderCalculatorǁadd_item__mutmut_16, 
        'xǁOrderCalculatorǁadd_item__mutmut_17': xǁOrderCalculatorǁadd_item__mutmut_17, 
        'xǁOrderCalculatorǁadd_item__mutmut_18': xǁOrderCalculatorǁadd_item__mutmut_18, 
        'xǁOrderCalculatorǁadd_item__mutmut_19': xǁOrderCalculatorǁadd_item__mutmut_19, 
        'xǁOrderCalculatorǁadd_item__mutmut_20': xǁOrderCalculatorǁadd_item__mutmut_20, 
        'xǁOrderCalculatorǁadd_item__mutmut_21': xǁOrderCalculatorǁadd_item__mutmut_21, 
        'xǁOrderCalculatorǁadd_item__mutmut_22': xǁOrderCalculatorǁadd_item__mutmut_22, 
        'xǁOrderCalculatorǁadd_item__mutmut_23': xǁOrderCalculatorǁadd_item__mutmut_23, 
        'xǁOrderCalculatorǁadd_item__mutmut_24': xǁOrderCalculatorǁadd_item__mutmut_24, 
        'xǁOrderCalculatorǁadd_item__mutmut_25': xǁOrderCalculatorǁadd_item__mutmut_25, 
        'xǁOrderCalculatorǁadd_item__mutmut_26': xǁOrderCalculatorǁadd_item__mutmut_26, 
        'xǁOrderCalculatorǁadd_item__mutmut_27': xǁOrderCalculatorǁadd_item__mutmut_27, 
        'xǁOrderCalculatorǁadd_item__mutmut_28': xǁOrderCalculatorǁadd_item__mutmut_28, 
        'xǁOrderCalculatorǁadd_item__mutmut_29': xǁOrderCalculatorǁadd_item__mutmut_29, 
        'xǁOrderCalculatorǁadd_item__mutmut_30': xǁOrderCalculatorǁadd_item__mutmut_30, 
        'xǁOrderCalculatorǁadd_item__mutmut_31': xǁOrderCalculatorǁadd_item__mutmut_31, 
        'xǁOrderCalculatorǁadd_item__mutmut_32': xǁOrderCalculatorǁadd_item__mutmut_32, 
        'xǁOrderCalculatorǁadd_item__mutmut_33': xǁOrderCalculatorǁadd_item__mutmut_33, 
        'xǁOrderCalculatorǁadd_item__mutmut_34': xǁOrderCalculatorǁadd_item__mutmut_34, 
        'xǁOrderCalculatorǁadd_item__mutmut_35': xǁOrderCalculatorǁadd_item__mutmut_35, 
        'xǁOrderCalculatorǁadd_item__mutmut_36': xǁOrderCalculatorǁadd_item__mutmut_36, 
        'xǁOrderCalculatorǁadd_item__mutmut_37': xǁOrderCalculatorǁadd_item__mutmut_37, 
        'xǁOrderCalculatorǁadd_item__mutmut_38': xǁOrderCalculatorǁadd_item__mutmut_38, 
        'xǁOrderCalculatorǁadd_item__mutmut_39': xǁOrderCalculatorǁadd_item__mutmut_39, 
        'xǁOrderCalculatorǁadd_item__mutmut_40': xǁOrderCalculatorǁadd_item__mutmut_40, 
        'xǁOrderCalculatorǁadd_item__mutmut_41': xǁOrderCalculatorǁadd_item__mutmut_41, 
        'xǁOrderCalculatorǁadd_item__mutmut_42': xǁOrderCalculatorǁadd_item__mutmut_42, 
        'xǁOrderCalculatorǁadd_item__mutmut_43': xǁOrderCalculatorǁadd_item__mutmut_43, 
        'xǁOrderCalculatorǁadd_item__mutmut_44': xǁOrderCalculatorǁadd_item__mutmut_44, 
        'xǁOrderCalculatorǁadd_item__mutmut_45': xǁOrderCalculatorǁadd_item__mutmut_45, 
        'xǁOrderCalculatorǁadd_item__mutmut_46': xǁOrderCalculatorǁadd_item__mutmut_46, 
        'xǁOrderCalculatorǁadd_item__mutmut_47': xǁOrderCalculatorǁadd_item__mutmut_47, 
        'xǁOrderCalculatorǁadd_item__mutmut_48': xǁOrderCalculatorǁadd_item__mutmut_48, 
        'xǁOrderCalculatorǁadd_item__mutmut_49': xǁOrderCalculatorǁadd_item__mutmut_49, 
        'xǁOrderCalculatorǁadd_item__mutmut_50': xǁOrderCalculatorǁadd_item__mutmut_50, 
        'xǁOrderCalculatorǁadd_item__mutmut_51': xǁOrderCalculatorǁadd_item__mutmut_51, 
        'xǁOrderCalculatorǁadd_item__mutmut_52': xǁOrderCalculatorǁadd_item__mutmut_52, 
        'xǁOrderCalculatorǁadd_item__mutmut_53': xǁOrderCalculatorǁadd_item__mutmut_53, 
        'xǁOrderCalculatorǁadd_item__mutmut_54': xǁOrderCalculatorǁadd_item__mutmut_54, 
        'xǁOrderCalculatorǁadd_item__mutmut_55': xǁOrderCalculatorǁadd_item__mutmut_55, 
        'xǁOrderCalculatorǁadd_item__mutmut_56': xǁOrderCalculatorǁadd_item__mutmut_56, 
        'xǁOrderCalculatorǁadd_item__mutmut_57': xǁOrderCalculatorǁadd_item__mutmut_57, 
        'xǁOrderCalculatorǁadd_item__mutmut_58': xǁOrderCalculatorǁadd_item__mutmut_58, 
        'xǁOrderCalculatorǁadd_item__mutmut_59': xǁOrderCalculatorǁadd_item__mutmut_59, 
        'xǁOrderCalculatorǁadd_item__mutmut_60': xǁOrderCalculatorǁadd_item__mutmut_60
    }
    
    def add_item(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOrderCalculatorǁadd_item__mutmut_orig"), object.__getattribute__(self, "xǁOrderCalculatorǁadd_item__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_item.__signature__ = _mutmut_signature(xǁOrderCalculatorǁadd_item__mutmut_orig)
    xǁOrderCalculatorǁadd_item__mutmut_orig.__name__ = 'xǁOrderCalculatorǁadd_item'

    def xǁOrderCalculatorǁremove_item__mutmut_orig(self, name: str):
        """
        Removes an item from the order.

        :param name: The name of the item to remove.
        :raises ValueError: If no item with the given name exists in the order.
        :raises TypeError: If name is not a string.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not any(item["name"] == name for item in self.items):
            raise ValueError(f"Item with name '{name}' does not exist in the order.")

        self.items = [item for item in self.items if item["name"] != name]

    def xǁOrderCalculatorǁremove_item__mutmut_1(self, name: str):
        """
        Removes an item from the order.

        :param name: The name of the item to remove.
        :raises ValueError: If no item with the given name exists in the order.
        :raises TypeError: If name is not a string.
        """
        if isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not any(item["name"] == name for item in self.items):
            raise ValueError(f"Item with name '{name}' does not exist in the order.")

        self.items = [item for item in self.items if item["name"] != name]

    def xǁOrderCalculatorǁremove_item__mutmut_2(self, name: str):
        """
        Removes an item from the order.

        :param name: The name of the item to remove.
        :raises ValueError: If no item with the given name exists in the order.
        :raises TypeError: If name is not a string.
        """
        if not isinstance(name, str):
            raise TypeError(None)
        if not any(item["name"] == name for item in self.items):
            raise ValueError(f"Item with name '{name}' does not exist in the order.")

        self.items = [item for item in self.items if item["name"] != name]

    def xǁOrderCalculatorǁremove_item__mutmut_3(self, name: str):
        """
        Removes an item from the order.

        :param name: The name of the item to remove.
        :raises ValueError: If no item with the given name exists in the order.
        :raises TypeError: If name is not a string.
        """
        if not isinstance(name, str):
            raise TypeError("XXItem name must be a string.XX")
        if not any(item["name"] == name for item in self.items):
            raise ValueError(f"Item with name '{name}' does not exist in the order.")

        self.items = [item for item in self.items if item["name"] != name]

    def xǁOrderCalculatorǁremove_item__mutmut_4(self, name: str):
        """
        Removes an item from the order.

        :param name: The name of the item to remove.
        :raises ValueError: If no item with the given name exists in the order.
        :raises TypeError: If name is not a string.
        """
        if not isinstance(name, str):
            raise TypeError("item name must be a string.")
        if not any(item["name"] == name for item in self.items):
            raise ValueError(f"Item with name '{name}' does not exist in the order.")

        self.items = [item for item in self.items if item["name"] != name]

    def xǁOrderCalculatorǁremove_item__mutmut_5(self, name: str):
        """
        Removes an item from the order.

        :param name: The name of the item to remove.
        :raises ValueError: If no item with the given name exists in the order.
        :raises TypeError: If name is not a string.
        """
        if not isinstance(name, str):
            raise TypeError("ITEM NAME MUST BE A STRING.")
        if not any(item["name"] == name for item in self.items):
            raise ValueError(f"Item with name '{name}' does not exist in the order.")

        self.items = [item for item in self.items if item["name"] != name]

    def xǁOrderCalculatorǁremove_item__mutmut_6(self, name: str):
        """
        Removes an item from the order.

        :param name: The name of the item to remove.
        :raises ValueError: If no item with the given name exists in the order.
        :raises TypeError: If name is not a string.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if any(item["name"] == name for item in self.items):
            raise ValueError(f"Item with name '{name}' does not exist in the order.")

        self.items = [item for item in self.items if item["name"] != name]

    def xǁOrderCalculatorǁremove_item__mutmut_7(self, name: str):
        """
        Removes an item from the order.

        :param name: The name of the item to remove.
        :raises ValueError: If no item with the given name exists in the order.
        :raises TypeError: If name is not a string.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not any(None):
            raise ValueError(f"Item with name '{name}' does not exist in the order.")

        self.items = [item for item in self.items if item["name"] != name]

    def xǁOrderCalculatorǁremove_item__mutmut_8(self, name: str):
        """
        Removes an item from the order.

        :param name: The name of the item to remove.
        :raises ValueError: If no item with the given name exists in the order.
        :raises TypeError: If name is not a string.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not any(item["XXnameXX"] == name for item in self.items):
            raise ValueError(f"Item with name '{name}' does not exist in the order.")

        self.items = [item for item in self.items if item["name"] != name]

    def xǁOrderCalculatorǁremove_item__mutmut_9(self, name: str):
        """
        Removes an item from the order.

        :param name: The name of the item to remove.
        :raises ValueError: If no item with the given name exists in the order.
        :raises TypeError: If name is not a string.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not any(item["NAME"] == name for item in self.items):
            raise ValueError(f"Item with name '{name}' does not exist in the order.")

        self.items = [item for item in self.items if item["name"] != name]

    def xǁOrderCalculatorǁremove_item__mutmut_10(self, name: str):
        """
        Removes an item from the order.

        :param name: The name of the item to remove.
        :raises ValueError: If no item with the given name exists in the order.
        :raises TypeError: If name is not a string.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not any(item["Name"] == name for item in self.items):
            raise ValueError(f"Item with name '{name}' does not exist in the order.")

        self.items = [item for item in self.items if item["name"] != name]

    def xǁOrderCalculatorǁremove_item__mutmut_11(self, name: str):
        """
        Removes an item from the order.

        :param name: The name of the item to remove.
        :raises ValueError: If no item with the given name exists in the order.
        :raises TypeError: If name is not a string.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not any(item["name"] != name for item in self.items):
            raise ValueError(f"Item with name '{name}' does not exist in the order.")

        self.items = [item for item in self.items if item["name"] != name]

    def xǁOrderCalculatorǁremove_item__mutmut_12(self, name: str):
        """
        Removes an item from the order.

        :param name: The name of the item to remove.
        :raises ValueError: If no item with the given name exists in the order.
        :raises TypeError: If name is not a string.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not any(item["name"] == name for item in self.items):
            raise ValueError(None)

        self.items = [item for item in self.items if item["name"] != name]

    def xǁOrderCalculatorǁremove_item__mutmut_13(self, name: str):
        """
        Removes an item from the order.

        :param name: The name of the item to remove.
        :raises ValueError: If no item with the given name exists in the order.
        :raises TypeError: If name is not a string.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not any(item["name"] == name for item in self.items):
            raise ValueError(f"Item with name '{name}' does not exist in the order.")

        self.items = None

    def xǁOrderCalculatorǁremove_item__mutmut_14(self, name: str):
        """
        Removes an item from the order.

        :param name: The name of the item to remove.
        :raises ValueError: If no item with the given name exists in the order.
        :raises TypeError: If name is not a string.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not any(item["name"] == name for item in self.items):
            raise ValueError(f"Item with name '{name}' does not exist in the order.")

        self.items = [item for item in self.items if item["XXnameXX"] != name]

    def xǁOrderCalculatorǁremove_item__mutmut_15(self, name: str):
        """
        Removes an item from the order.

        :param name: The name of the item to remove.
        :raises ValueError: If no item with the given name exists in the order.
        :raises TypeError: If name is not a string.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not any(item["name"] == name for item in self.items):
            raise ValueError(f"Item with name '{name}' does not exist in the order.")

        self.items = [item for item in self.items if item["NAME"] != name]

    def xǁOrderCalculatorǁremove_item__mutmut_16(self, name: str):
        """
        Removes an item from the order.

        :param name: The name of the item to remove.
        :raises ValueError: If no item with the given name exists in the order.
        :raises TypeError: If name is not a string.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not any(item["name"] == name for item in self.items):
            raise ValueError(f"Item with name '{name}' does not exist in the order.")

        self.items = [item for item in self.items if item["Name"] != name]

    def xǁOrderCalculatorǁremove_item__mutmut_17(self, name: str):
        """
        Removes an item from the order.

        :param name: The name of the item to remove.
        :raises ValueError: If no item with the given name exists in the order.
        :raises TypeError: If name is not a string.
        """
        if not isinstance(name, str):
            raise TypeError("Item name must be a string.")
        if not any(item["name"] == name for item in self.items):
            raise ValueError(f"Item with name '{name}' does not exist in the order.")

        self.items = [item for item in self.items if item["name"] == name]
    
    xǁOrderCalculatorǁremove_item__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOrderCalculatorǁremove_item__mutmut_1': xǁOrderCalculatorǁremove_item__mutmut_1, 
        'xǁOrderCalculatorǁremove_item__mutmut_2': xǁOrderCalculatorǁremove_item__mutmut_2, 
        'xǁOrderCalculatorǁremove_item__mutmut_3': xǁOrderCalculatorǁremove_item__mutmut_3, 
        'xǁOrderCalculatorǁremove_item__mutmut_4': xǁOrderCalculatorǁremove_item__mutmut_4, 
        'xǁOrderCalculatorǁremove_item__mutmut_5': xǁOrderCalculatorǁremove_item__mutmut_5, 
        'xǁOrderCalculatorǁremove_item__mutmut_6': xǁOrderCalculatorǁremove_item__mutmut_6, 
        'xǁOrderCalculatorǁremove_item__mutmut_7': xǁOrderCalculatorǁremove_item__mutmut_7, 
        'xǁOrderCalculatorǁremove_item__mutmut_8': xǁOrderCalculatorǁremove_item__mutmut_8, 
        'xǁOrderCalculatorǁremove_item__mutmut_9': xǁOrderCalculatorǁremove_item__mutmut_9, 
        'xǁOrderCalculatorǁremove_item__mutmut_10': xǁOrderCalculatorǁremove_item__mutmut_10, 
        'xǁOrderCalculatorǁremove_item__mutmut_11': xǁOrderCalculatorǁremove_item__mutmut_11, 
        'xǁOrderCalculatorǁremove_item__mutmut_12': xǁOrderCalculatorǁremove_item__mutmut_12, 
        'xǁOrderCalculatorǁremove_item__mutmut_13': xǁOrderCalculatorǁremove_item__mutmut_13, 
        'xǁOrderCalculatorǁremove_item__mutmut_14': xǁOrderCalculatorǁremove_item__mutmut_14, 
        'xǁOrderCalculatorǁremove_item__mutmut_15': xǁOrderCalculatorǁremove_item__mutmut_15, 
        'xǁOrderCalculatorǁremove_item__mutmut_16': xǁOrderCalculatorǁremove_item__mutmut_16, 
        'xǁOrderCalculatorǁremove_item__mutmut_17': xǁOrderCalculatorǁremove_item__mutmut_17
    }
    
    def remove_item(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOrderCalculatorǁremove_item__mutmut_orig"), object.__getattribute__(self, "xǁOrderCalculatorǁremove_item__mutmut_mutants"), args, kwargs, self)
        return result 
    
    remove_item.__signature__ = _mutmut_signature(xǁOrderCalculatorǁremove_item__mutmut_orig)
    xǁOrderCalculatorǁremove_item__mutmut_orig.__name__ = 'xǁOrderCalculatorǁremove_item'

    def xǁOrderCalculatorǁget_subtotal__mutmut_orig(self) -> float:
        """
        Calculates the subtotal (sum of item prices times their quantities) for all items in the order.

        :return: The subtotal as a float.
        :raises ValueError: If the order is empty.
        """
        if not self.items:
            raise ValueError("Cannot calculate subtotal on empty order.")
        return sum(item["price"] * item["quantity"] for item in self.items)

    def xǁOrderCalculatorǁget_subtotal__mutmut_1(self) -> float:
        """
        Calculates the subtotal (sum of item prices times their quantities) for all items in the order.

        :return: The subtotal as a float.
        :raises ValueError: If the order is empty.
        """
        if self.items:
            raise ValueError("Cannot calculate subtotal on empty order.")
        return sum(item["price"] * item["quantity"] for item in self.items)

    def xǁOrderCalculatorǁget_subtotal__mutmut_2(self) -> float:
        """
        Calculates the subtotal (sum of item prices times their quantities) for all items in the order.

        :return: The subtotal as a float.
        :raises ValueError: If the order is empty.
        """
        if not self.items:
            raise ValueError(None)
        return sum(item["price"] * item["quantity"] for item in self.items)

    def xǁOrderCalculatorǁget_subtotal__mutmut_3(self) -> float:
        """
        Calculates the subtotal (sum of item prices times their quantities) for all items in the order.

        :return: The subtotal as a float.
        :raises ValueError: If the order is empty.
        """
        if not self.items:
            raise ValueError("XXCannot calculate subtotal on empty order.XX")
        return sum(item["price"] * item["quantity"] for item in self.items)

    def xǁOrderCalculatorǁget_subtotal__mutmut_4(self) -> float:
        """
        Calculates the subtotal (sum of item prices times their quantities) for all items in the order.

        :return: The subtotal as a float.
        :raises ValueError: If the order is empty.
        """
        if not self.items:
            raise ValueError("cannot calculate subtotal on empty order.")
        return sum(item["price"] * item["quantity"] for item in self.items)

    def xǁOrderCalculatorǁget_subtotal__mutmut_5(self) -> float:
        """
        Calculates the subtotal (sum of item prices times their quantities) for all items in the order.

        :return: The subtotal as a float.
        :raises ValueError: If the order is empty.
        """
        if not self.items:
            raise ValueError("CANNOT CALCULATE SUBTOTAL ON EMPTY ORDER.")
        return sum(item["price"] * item["quantity"] for item in self.items)

    def xǁOrderCalculatorǁget_subtotal__mutmut_6(self) -> float:
        """
        Calculates the subtotal (sum of item prices times their quantities) for all items in the order.

        :return: The subtotal as a float.
        :raises ValueError: If the order is empty.
        """
        if not self.items:
            raise ValueError("Cannot calculate subtotal on empty order.")
        return sum(None)

    def xǁOrderCalculatorǁget_subtotal__mutmut_7(self) -> float:
        """
        Calculates the subtotal (sum of item prices times their quantities) for all items in the order.

        :return: The subtotal as a float.
        :raises ValueError: If the order is empty.
        """
        if not self.items:
            raise ValueError("Cannot calculate subtotal on empty order.")
        return sum(item["XXpriceXX"] * item["quantity"] for item in self.items)

    def xǁOrderCalculatorǁget_subtotal__mutmut_8(self) -> float:
        """
        Calculates the subtotal (sum of item prices times their quantities) for all items in the order.

        :return: The subtotal as a float.
        :raises ValueError: If the order is empty.
        """
        if not self.items:
            raise ValueError("Cannot calculate subtotal on empty order.")
        return sum(item["PRICE"] * item["quantity"] for item in self.items)

    def xǁOrderCalculatorǁget_subtotal__mutmut_9(self) -> float:
        """
        Calculates the subtotal (sum of item prices times their quantities) for all items in the order.

        :return: The subtotal as a float.
        :raises ValueError: If the order is empty.
        """
        if not self.items:
            raise ValueError("Cannot calculate subtotal on empty order.")
        return sum(item["Price"] * item["quantity"] for item in self.items)

    def xǁOrderCalculatorǁget_subtotal__mutmut_10(self) -> float:
        """
        Calculates the subtotal (sum of item prices times their quantities) for all items in the order.

        :return: The subtotal as a float.
        :raises ValueError: If the order is empty.
        """
        if not self.items:
            raise ValueError("Cannot calculate subtotal on empty order.")
        return sum(item["price"] / item["quantity"] for item in self.items)

    def xǁOrderCalculatorǁget_subtotal__mutmut_11(self) -> float:
        """
        Calculates the subtotal (sum of item prices times their quantities) for all items in the order.

        :return: The subtotal as a float.
        :raises ValueError: If the order is empty.
        """
        if not self.items:
            raise ValueError("Cannot calculate subtotal on empty order.")
        return sum(item["price"] * item["XXquantityXX"] for item in self.items)

    def xǁOrderCalculatorǁget_subtotal__mutmut_12(self) -> float:
        """
        Calculates the subtotal (sum of item prices times their quantities) for all items in the order.

        :return: The subtotal as a float.
        :raises ValueError: If the order is empty.
        """
        if not self.items:
            raise ValueError("Cannot calculate subtotal on empty order.")
        return sum(item["price"] * item["QUANTITY"] for item in self.items)

    def xǁOrderCalculatorǁget_subtotal__mutmut_13(self) -> float:
        """
        Calculates the subtotal (sum of item prices times their quantities) for all items in the order.

        :return: The subtotal as a float.
        :raises ValueError: If the order is empty.
        """
        if not self.items:
            raise ValueError("Cannot calculate subtotal on empty order.")
        return sum(item["price"] * item["Quantity"] for item in self.items)
    
    xǁOrderCalculatorǁget_subtotal__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOrderCalculatorǁget_subtotal__mutmut_1': xǁOrderCalculatorǁget_subtotal__mutmut_1, 
        'xǁOrderCalculatorǁget_subtotal__mutmut_2': xǁOrderCalculatorǁget_subtotal__mutmut_2, 
        'xǁOrderCalculatorǁget_subtotal__mutmut_3': xǁOrderCalculatorǁget_subtotal__mutmut_3, 
        'xǁOrderCalculatorǁget_subtotal__mutmut_4': xǁOrderCalculatorǁget_subtotal__mutmut_4, 
        'xǁOrderCalculatorǁget_subtotal__mutmut_5': xǁOrderCalculatorǁget_subtotal__mutmut_5, 
        'xǁOrderCalculatorǁget_subtotal__mutmut_6': xǁOrderCalculatorǁget_subtotal__mutmut_6, 
        'xǁOrderCalculatorǁget_subtotal__mutmut_7': xǁOrderCalculatorǁget_subtotal__mutmut_7, 
        'xǁOrderCalculatorǁget_subtotal__mutmut_8': xǁOrderCalculatorǁget_subtotal__mutmut_8, 
        'xǁOrderCalculatorǁget_subtotal__mutmut_9': xǁOrderCalculatorǁget_subtotal__mutmut_9, 
        'xǁOrderCalculatorǁget_subtotal__mutmut_10': xǁOrderCalculatorǁget_subtotal__mutmut_10, 
        'xǁOrderCalculatorǁget_subtotal__mutmut_11': xǁOrderCalculatorǁget_subtotal__mutmut_11, 
        'xǁOrderCalculatorǁget_subtotal__mutmut_12': xǁOrderCalculatorǁget_subtotal__mutmut_12, 
        'xǁOrderCalculatorǁget_subtotal__mutmut_13': xǁOrderCalculatorǁget_subtotal__mutmut_13
    }
    
    def get_subtotal(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOrderCalculatorǁget_subtotal__mutmut_orig"), object.__getattribute__(self, "xǁOrderCalculatorǁget_subtotal__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_subtotal.__signature__ = _mutmut_signature(xǁOrderCalculatorǁget_subtotal__mutmut_orig)
    xǁOrderCalculatorǁget_subtotal__mutmut_orig.__name__ = 'xǁOrderCalculatorǁget_subtotal'

    def xǁOrderCalculatorǁapply_discount__mutmut_orig(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("Subtotal must be a number.")
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")
        if not 0.0 <= discount <= 1.0:
            raise ValueError("Discount must be between 0.0 and 1.0.")
        if subtotal < 0.0:
            raise ValueError("Cannot apply discount on negative subtotal.")
        return subtotal * (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_1(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if isinstance(subtotal, (float, int)):
            raise TypeError("Subtotal must be a number.")
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")
        if not 0.0 <= discount <= 1.0:
            raise ValueError("Discount must be between 0.0 and 1.0.")
        if subtotal < 0.0:
            raise ValueError("Cannot apply discount on negative subtotal.")
        return subtotal * (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_2(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError(None)
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")
        if not 0.0 <= discount <= 1.0:
            raise ValueError("Discount must be between 0.0 and 1.0.")
        if subtotal < 0.0:
            raise ValueError("Cannot apply discount on negative subtotal.")
        return subtotal * (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_3(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("XXSubtotal must be a number.XX")
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")
        if not 0.0 <= discount <= 1.0:
            raise ValueError("Discount must be between 0.0 and 1.0.")
        if subtotal < 0.0:
            raise ValueError("Cannot apply discount on negative subtotal.")
        return subtotal * (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_4(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("subtotal must be a number.")
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")
        if not 0.0 <= discount <= 1.0:
            raise ValueError("Discount must be between 0.0 and 1.0.")
        if subtotal < 0.0:
            raise ValueError("Cannot apply discount on negative subtotal.")
        return subtotal * (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_5(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("SUBTOTAL MUST BE A NUMBER.")
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")
        if not 0.0 <= discount <= 1.0:
            raise ValueError("Discount must be between 0.0 and 1.0.")
        if subtotal < 0.0:
            raise ValueError("Cannot apply discount on negative subtotal.")
        return subtotal * (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_6(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("Subtotal must be a number.")
        if isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")
        if not 0.0 <= discount <= 1.0:
            raise ValueError("Discount must be between 0.0 and 1.0.")
        if subtotal < 0.0:
            raise ValueError("Cannot apply discount on negative subtotal.")
        return subtotal * (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_7(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("Subtotal must be a number.")
        if not isinstance(discount, (float, int)):
            raise TypeError(None)
        if not 0.0 <= discount <= 1.0:
            raise ValueError("Discount must be between 0.0 and 1.0.")
        if subtotal < 0.0:
            raise ValueError("Cannot apply discount on negative subtotal.")
        return subtotal * (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_8(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("Subtotal must be a number.")
        if not isinstance(discount, (float, int)):
            raise TypeError("XXDiscount must be a number.XX")
        if not 0.0 <= discount <= 1.0:
            raise ValueError("Discount must be between 0.0 and 1.0.")
        if subtotal < 0.0:
            raise ValueError("Cannot apply discount on negative subtotal.")
        return subtotal * (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_9(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("Subtotal must be a number.")
        if not isinstance(discount, (float, int)):
            raise TypeError("discount must be a number.")
        if not 0.0 <= discount <= 1.0:
            raise ValueError("Discount must be between 0.0 and 1.0.")
        if subtotal < 0.0:
            raise ValueError("Cannot apply discount on negative subtotal.")
        return subtotal * (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_10(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("Subtotal must be a number.")
        if not isinstance(discount, (float, int)):
            raise TypeError("DISCOUNT MUST BE A NUMBER.")
        if not 0.0 <= discount <= 1.0:
            raise ValueError("Discount must be between 0.0 and 1.0.")
        if subtotal < 0.0:
            raise ValueError("Cannot apply discount on negative subtotal.")
        return subtotal * (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_11(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("Subtotal must be a number.")
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")
        if 0.0 <= discount <= 1.0:
            raise ValueError("Discount must be between 0.0 and 1.0.")
        if subtotal < 0.0:
            raise ValueError("Cannot apply discount on negative subtotal.")
        return subtotal * (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_12(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("Subtotal must be a number.")
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")
        if not 1.0 <= discount <= 1.0:
            raise ValueError("Discount must be between 0.0 and 1.0.")
        if subtotal < 0.0:
            raise ValueError("Cannot apply discount on negative subtotal.")
        return subtotal * (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_13(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("Subtotal must be a number.")
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")
        if not 0.0 < discount <= 1.0:
            raise ValueError("Discount must be between 0.0 and 1.0.")
        if subtotal < 0.0:
            raise ValueError("Cannot apply discount on negative subtotal.")
        return subtotal * (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_14(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("Subtotal must be a number.")
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")
        if not 0.0 <= discount < 1.0:
            raise ValueError("Discount must be between 0.0 and 1.0.")
        if subtotal < 0.0:
            raise ValueError("Cannot apply discount on negative subtotal.")
        return subtotal * (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_15(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("Subtotal must be a number.")
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")
        if not 0.0 <= discount <= 2.0:
            raise ValueError("Discount must be between 0.0 and 1.0.")
        if subtotal < 0.0:
            raise ValueError("Cannot apply discount on negative subtotal.")
        return subtotal * (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_16(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("Subtotal must be a number.")
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")
        if not 0.0 <= discount <= 1.0:
            raise ValueError(None)
        if subtotal < 0.0:
            raise ValueError("Cannot apply discount on negative subtotal.")
        return subtotal * (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_17(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("Subtotal must be a number.")
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")
        if not 0.0 <= discount <= 1.0:
            raise ValueError("XXDiscount must be between 0.0 and 1.0.XX")
        if subtotal < 0.0:
            raise ValueError("Cannot apply discount on negative subtotal.")
        return subtotal * (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_18(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("Subtotal must be a number.")
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")
        if not 0.0 <= discount <= 1.0:
            raise ValueError("discount must be between 0.0 and 1.0.")
        if subtotal < 0.0:
            raise ValueError("Cannot apply discount on negative subtotal.")
        return subtotal * (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_19(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("Subtotal must be a number.")
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")
        if not 0.0 <= discount <= 1.0:
            raise ValueError("DISCOUNT MUST BE BETWEEN 0.0 AND 1.0.")
        if subtotal < 0.0:
            raise ValueError("Cannot apply discount on negative subtotal.")
        return subtotal * (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_20(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("Subtotal must be a number.")
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")
        if not 0.0 <= discount <= 1.0:
            raise ValueError("Discount must be between 0.0 and 1.0.")
        if subtotal <= 0.0:
            raise ValueError("Cannot apply discount on negative subtotal.")
        return subtotal * (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_21(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("Subtotal must be a number.")
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")
        if not 0.0 <= discount <= 1.0:
            raise ValueError("Discount must be between 0.0 and 1.0.")
        if subtotal < 1.0:
            raise ValueError("Cannot apply discount on negative subtotal.")
        return subtotal * (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_22(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("Subtotal must be a number.")
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")
        if not 0.0 <= discount <= 1.0:
            raise ValueError("Discount must be between 0.0 and 1.0.")
        if subtotal < 0.0:
            raise ValueError(None)
        return subtotal * (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_23(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("Subtotal must be a number.")
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")
        if not 0.0 <= discount <= 1.0:
            raise ValueError("Discount must be between 0.0 and 1.0.")
        if subtotal < 0.0:
            raise ValueError("XXCannot apply discount on negative subtotal.XX")
        return subtotal * (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_24(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("Subtotal must be a number.")
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")
        if not 0.0 <= discount <= 1.0:
            raise ValueError("Discount must be between 0.0 and 1.0.")
        if subtotal < 0.0:
            raise ValueError("cannot apply discount on negative subtotal.")
        return subtotal * (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_25(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("Subtotal must be a number.")
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")
        if not 0.0 <= discount <= 1.0:
            raise ValueError("Discount must be between 0.0 and 1.0.")
        if subtotal < 0.0:
            raise ValueError("CANNOT APPLY DISCOUNT ON NEGATIVE SUBTOTAL.")
        return subtotal * (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_26(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("Subtotal must be a number.")
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")
        if not 0.0 <= discount <= 1.0:
            raise ValueError("Discount must be between 0.0 and 1.0.")
        if subtotal < 0.0:
            raise ValueError("Cannot apply discount on negative subtotal.")
        return subtotal / (1 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_27(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("Subtotal must be a number.")
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")
        if not 0.0 <= discount <= 1.0:
            raise ValueError("Discount must be between 0.0 and 1.0.")
        if subtotal < 0.0:
            raise ValueError("Cannot apply discount on negative subtotal.")
        return subtotal * (2 - discount)

    def xǁOrderCalculatorǁapply_discount__mutmut_28(self, subtotal: float, discount: float) -> float:
        """
        Applies a percentage discount to the given subtotal.

        :param subtotal: the subtotal amount (must be >= 0)
        :param discount: the discount rate as a float between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The discounted subtotal.
        :raises ValueError: If subtotal < 0 or discount is outside the [0.0, 1.0] range.
        :raises TypeError: If inputs are of incorrect types.
        """
        if not isinstance(subtotal, (float, int)):
            raise TypeError("Subtotal must be a number.")
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")
        if not 0.0 <= discount <= 1.0:
            raise ValueError("Discount must be between 0.0 and 1.0.")
        if subtotal < 0.0:
            raise ValueError("Cannot apply discount on negative subtotal.")
        return subtotal * (1 + discount)
    
    xǁOrderCalculatorǁapply_discount__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOrderCalculatorǁapply_discount__mutmut_1': xǁOrderCalculatorǁapply_discount__mutmut_1, 
        'xǁOrderCalculatorǁapply_discount__mutmut_2': xǁOrderCalculatorǁapply_discount__mutmut_2, 
        'xǁOrderCalculatorǁapply_discount__mutmut_3': xǁOrderCalculatorǁapply_discount__mutmut_3, 
        'xǁOrderCalculatorǁapply_discount__mutmut_4': xǁOrderCalculatorǁapply_discount__mutmut_4, 
        'xǁOrderCalculatorǁapply_discount__mutmut_5': xǁOrderCalculatorǁapply_discount__mutmut_5, 
        'xǁOrderCalculatorǁapply_discount__mutmut_6': xǁOrderCalculatorǁapply_discount__mutmut_6, 
        'xǁOrderCalculatorǁapply_discount__mutmut_7': xǁOrderCalculatorǁapply_discount__mutmut_7, 
        'xǁOrderCalculatorǁapply_discount__mutmut_8': xǁOrderCalculatorǁapply_discount__mutmut_8, 
        'xǁOrderCalculatorǁapply_discount__mutmut_9': xǁOrderCalculatorǁapply_discount__mutmut_9, 
        'xǁOrderCalculatorǁapply_discount__mutmut_10': xǁOrderCalculatorǁapply_discount__mutmut_10, 
        'xǁOrderCalculatorǁapply_discount__mutmut_11': xǁOrderCalculatorǁapply_discount__mutmut_11, 
        'xǁOrderCalculatorǁapply_discount__mutmut_12': xǁOrderCalculatorǁapply_discount__mutmut_12, 
        'xǁOrderCalculatorǁapply_discount__mutmut_13': xǁOrderCalculatorǁapply_discount__mutmut_13, 
        'xǁOrderCalculatorǁapply_discount__mutmut_14': xǁOrderCalculatorǁapply_discount__mutmut_14, 
        'xǁOrderCalculatorǁapply_discount__mutmut_15': xǁOrderCalculatorǁapply_discount__mutmut_15, 
        'xǁOrderCalculatorǁapply_discount__mutmut_16': xǁOrderCalculatorǁapply_discount__mutmut_16, 
        'xǁOrderCalculatorǁapply_discount__mutmut_17': xǁOrderCalculatorǁapply_discount__mutmut_17, 
        'xǁOrderCalculatorǁapply_discount__mutmut_18': xǁOrderCalculatorǁapply_discount__mutmut_18, 
        'xǁOrderCalculatorǁapply_discount__mutmut_19': xǁOrderCalculatorǁapply_discount__mutmut_19, 
        'xǁOrderCalculatorǁapply_discount__mutmut_20': xǁOrderCalculatorǁapply_discount__mutmut_20, 
        'xǁOrderCalculatorǁapply_discount__mutmut_21': xǁOrderCalculatorǁapply_discount__mutmut_21, 
        'xǁOrderCalculatorǁapply_discount__mutmut_22': xǁOrderCalculatorǁapply_discount__mutmut_22, 
        'xǁOrderCalculatorǁapply_discount__mutmut_23': xǁOrderCalculatorǁapply_discount__mutmut_23, 
        'xǁOrderCalculatorǁapply_discount__mutmut_24': xǁOrderCalculatorǁapply_discount__mutmut_24, 
        'xǁOrderCalculatorǁapply_discount__mutmut_25': xǁOrderCalculatorǁapply_discount__mutmut_25, 
        'xǁOrderCalculatorǁapply_discount__mutmut_26': xǁOrderCalculatorǁapply_discount__mutmut_26, 
        'xǁOrderCalculatorǁapply_discount__mutmut_27': xǁOrderCalculatorǁapply_discount__mutmut_27, 
        'xǁOrderCalculatorǁapply_discount__mutmut_28': xǁOrderCalculatorǁapply_discount__mutmut_28
    }
    
    def apply_discount(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOrderCalculatorǁapply_discount__mutmut_orig"), object.__getattribute__(self, "xǁOrderCalculatorǁapply_discount__mutmut_mutants"), args, kwargs, self)
        return result 
    
    apply_discount.__signature__ = _mutmut_signature(xǁOrderCalculatorǁapply_discount__mutmut_orig)
    xǁOrderCalculatorǁapply_discount__mutmut_orig.__name__ = 'xǁOrderCalculatorǁapply_discount'

    def xǁOrderCalculatorǁcalculate_shipping__mutmut_orig(self, discounted_subtotal: float) -> float:
        """
        Calculates the shipping cost based on the discounted subtotal.

        If the discounted subtotal >= free shipping threshold shipping is free (0.0).
        Otherwise, the standard shipping cost is applied.

        :param discounted_subtotal: The subtotal amount after applying discount (must be >= 0.0).
        :return: The shipping cost as a float (0.0 or self.shipping_cost).
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discounted_subtotal, (float, int)):
            raise TypeError("Discounted subtotal must be a number.")
        if discounted_subtotal >= self.free_shipping_threshold:
            return 0.0
        return self.shipping_cost

    def xǁOrderCalculatorǁcalculate_shipping__mutmut_1(self, discounted_subtotal: float) -> float:
        """
        Calculates the shipping cost based on the discounted subtotal.

        If the discounted subtotal >= free shipping threshold shipping is free (0.0).
        Otherwise, the standard shipping cost is applied.

        :param discounted_subtotal: The subtotal amount after applying discount (must be >= 0.0).
        :return: The shipping cost as a float (0.0 or self.shipping_cost).
        :raises TypeError: If input is not a number.
        """
        if isinstance(discounted_subtotal, (float, int)):
            raise TypeError("Discounted subtotal must be a number.")
        if discounted_subtotal >= self.free_shipping_threshold:
            return 0.0
        return self.shipping_cost

    def xǁOrderCalculatorǁcalculate_shipping__mutmut_2(self, discounted_subtotal: float) -> float:
        """
        Calculates the shipping cost based on the discounted subtotal.

        If the discounted subtotal >= free shipping threshold shipping is free (0.0).
        Otherwise, the standard shipping cost is applied.

        :param discounted_subtotal: The subtotal amount after applying discount (must be >= 0.0).
        :return: The shipping cost as a float (0.0 or self.shipping_cost).
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discounted_subtotal, (float, int)):
            raise TypeError(None)
        if discounted_subtotal >= self.free_shipping_threshold:
            return 0.0
        return self.shipping_cost

    def xǁOrderCalculatorǁcalculate_shipping__mutmut_3(self, discounted_subtotal: float) -> float:
        """
        Calculates the shipping cost based on the discounted subtotal.

        If the discounted subtotal >= free shipping threshold shipping is free (0.0).
        Otherwise, the standard shipping cost is applied.

        :param discounted_subtotal: The subtotal amount after applying discount (must be >= 0.0).
        :return: The shipping cost as a float (0.0 or self.shipping_cost).
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discounted_subtotal, (float, int)):
            raise TypeError("XXDiscounted subtotal must be a number.XX")
        if discounted_subtotal >= self.free_shipping_threshold:
            return 0.0
        return self.shipping_cost

    def xǁOrderCalculatorǁcalculate_shipping__mutmut_4(self, discounted_subtotal: float) -> float:
        """
        Calculates the shipping cost based on the discounted subtotal.

        If the discounted subtotal >= free shipping threshold shipping is free (0.0).
        Otherwise, the standard shipping cost is applied.

        :param discounted_subtotal: The subtotal amount after applying discount (must be >= 0.0).
        :return: The shipping cost as a float (0.0 or self.shipping_cost).
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discounted_subtotal, (float, int)):
            raise TypeError("discounted subtotal must be a number.")
        if discounted_subtotal >= self.free_shipping_threshold:
            return 0.0
        return self.shipping_cost

    def xǁOrderCalculatorǁcalculate_shipping__mutmut_5(self, discounted_subtotal: float) -> float:
        """
        Calculates the shipping cost based on the discounted subtotal.

        If the discounted subtotal >= free shipping threshold shipping is free (0.0).
        Otherwise, the standard shipping cost is applied.

        :param discounted_subtotal: The subtotal amount after applying discount (must be >= 0.0).
        :return: The shipping cost as a float (0.0 or self.shipping_cost).
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discounted_subtotal, (float, int)):
            raise TypeError("DISCOUNTED SUBTOTAL MUST BE A NUMBER.")
        if discounted_subtotal >= self.free_shipping_threshold:
            return 0.0
        return self.shipping_cost

    def xǁOrderCalculatorǁcalculate_shipping__mutmut_6(self, discounted_subtotal: float) -> float:
        """
        Calculates the shipping cost based on the discounted subtotal.

        If the discounted subtotal >= free shipping threshold shipping is free (0.0).
        Otherwise, the standard shipping cost is applied.

        :param discounted_subtotal: The subtotal amount after applying discount (must be >= 0.0).
        :return: The shipping cost as a float (0.0 or self.shipping_cost).
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discounted_subtotal, (float, int)):
            raise TypeError("Discounted subtotal must be a number.")
        if discounted_subtotal > self.free_shipping_threshold:
            return 0.0
        return self.shipping_cost

    def xǁOrderCalculatorǁcalculate_shipping__mutmut_7(self, discounted_subtotal: float) -> float:
        """
        Calculates the shipping cost based on the discounted subtotal.

        If the discounted subtotal >= free shipping threshold shipping is free (0.0).
        Otherwise, the standard shipping cost is applied.

        :param discounted_subtotal: The subtotal amount after applying discount (must be >= 0.0).
        :return: The shipping cost as a float (0.0 or self.shipping_cost).
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discounted_subtotal, (float, int)):
            raise TypeError("Discounted subtotal must be a number.")
        if discounted_subtotal >= self.free_shipping_threshold:
            return 1.0
        return self.shipping_cost
    
    xǁOrderCalculatorǁcalculate_shipping__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOrderCalculatorǁcalculate_shipping__mutmut_1': xǁOrderCalculatorǁcalculate_shipping__mutmut_1, 
        'xǁOrderCalculatorǁcalculate_shipping__mutmut_2': xǁOrderCalculatorǁcalculate_shipping__mutmut_2, 
        'xǁOrderCalculatorǁcalculate_shipping__mutmut_3': xǁOrderCalculatorǁcalculate_shipping__mutmut_3, 
        'xǁOrderCalculatorǁcalculate_shipping__mutmut_4': xǁOrderCalculatorǁcalculate_shipping__mutmut_4, 
        'xǁOrderCalculatorǁcalculate_shipping__mutmut_5': xǁOrderCalculatorǁcalculate_shipping__mutmut_5, 
        'xǁOrderCalculatorǁcalculate_shipping__mutmut_6': xǁOrderCalculatorǁcalculate_shipping__mutmut_6, 
        'xǁOrderCalculatorǁcalculate_shipping__mutmut_7': xǁOrderCalculatorǁcalculate_shipping__mutmut_7
    }
    
    def calculate_shipping(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOrderCalculatorǁcalculate_shipping__mutmut_orig"), object.__getattribute__(self, "xǁOrderCalculatorǁcalculate_shipping__mutmut_mutants"), args, kwargs, self)
        return result 
    
    calculate_shipping.__signature__ = _mutmut_signature(xǁOrderCalculatorǁcalculate_shipping__mutmut_orig)
    xǁOrderCalculatorǁcalculate_shipping__mutmut_orig.__name__ = 'xǁOrderCalculatorǁcalculate_shipping'

    def xǁOrderCalculatorǁcalculate_tax__mutmut_orig(self, amount: float) -> float:
        """
        Calculates the tax based on the provided amount using the configured tax rate.

        :param amount: The amount on which to calculate the tax (must be >= 0.0).
        :return: The tax as a float.
        :raises ValueError: If the amount is negative.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(amount, (float, int)):
            raise TypeError("Amount must be a number.")
        if amount < 0.0:
            raise ValueError("Cannot calculate tax on negative amount.")
        return amount * self.tax_rate

    def xǁOrderCalculatorǁcalculate_tax__mutmut_1(self, amount: float) -> float:
        """
        Calculates the tax based on the provided amount using the configured tax rate.

        :param amount: The amount on which to calculate the tax (must be >= 0.0).
        :return: The tax as a float.
        :raises ValueError: If the amount is negative.
        :raises TypeError: If input is not a number.
        """
        if isinstance(amount, (float, int)):
            raise TypeError("Amount must be a number.")
        if amount < 0.0:
            raise ValueError("Cannot calculate tax on negative amount.")
        return amount * self.tax_rate

    def xǁOrderCalculatorǁcalculate_tax__mutmut_2(self, amount: float) -> float:
        """
        Calculates the tax based on the provided amount using the configured tax rate.

        :param amount: The amount on which to calculate the tax (must be >= 0.0).
        :return: The tax as a float.
        :raises ValueError: If the amount is negative.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(amount, (float, int)):
            raise TypeError(None)
        if amount < 0.0:
            raise ValueError("Cannot calculate tax on negative amount.")
        return amount * self.tax_rate

    def xǁOrderCalculatorǁcalculate_tax__mutmut_3(self, amount: float) -> float:
        """
        Calculates the tax based on the provided amount using the configured tax rate.

        :param amount: The amount on which to calculate the tax (must be >= 0.0).
        :return: The tax as a float.
        :raises ValueError: If the amount is negative.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(amount, (float, int)):
            raise TypeError("XXAmount must be a number.XX")
        if amount < 0.0:
            raise ValueError("Cannot calculate tax on negative amount.")
        return amount * self.tax_rate

    def xǁOrderCalculatorǁcalculate_tax__mutmut_4(self, amount: float) -> float:
        """
        Calculates the tax based on the provided amount using the configured tax rate.

        :param amount: The amount on which to calculate the tax (must be >= 0.0).
        :return: The tax as a float.
        :raises ValueError: If the amount is negative.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(amount, (float, int)):
            raise TypeError("amount must be a number.")
        if amount < 0.0:
            raise ValueError("Cannot calculate tax on negative amount.")
        return amount * self.tax_rate

    def xǁOrderCalculatorǁcalculate_tax__mutmut_5(self, amount: float) -> float:
        """
        Calculates the tax based on the provided amount using the configured tax rate.

        :param amount: The amount on which to calculate the tax (must be >= 0.0).
        :return: The tax as a float.
        :raises ValueError: If the amount is negative.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(amount, (float, int)):
            raise TypeError("AMOUNT MUST BE A NUMBER.")
        if amount < 0.0:
            raise ValueError("Cannot calculate tax on negative amount.")
        return amount * self.tax_rate

    def xǁOrderCalculatorǁcalculate_tax__mutmut_6(self, amount: float) -> float:
        """
        Calculates the tax based on the provided amount using the configured tax rate.

        :param amount: The amount on which to calculate the tax (must be >= 0.0).
        :return: The tax as a float.
        :raises ValueError: If the amount is negative.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(amount, (float, int)):
            raise TypeError("Amount must be a number.")
        if amount <= 0.0:
            raise ValueError("Cannot calculate tax on negative amount.")
        return amount * self.tax_rate

    def xǁOrderCalculatorǁcalculate_tax__mutmut_7(self, amount: float) -> float:
        """
        Calculates the tax based on the provided amount using the configured tax rate.

        :param amount: The amount on which to calculate the tax (must be >= 0.0).
        :return: The tax as a float.
        :raises ValueError: If the amount is negative.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(amount, (float, int)):
            raise TypeError("Amount must be a number.")
        if amount < 1.0:
            raise ValueError("Cannot calculate tax on negative amount.")
        return amount * self.tax_rate

    def xǁOrderCalculatorǁcalculate_tax__mutmut_8(self, amount: float) -> float:
        """
        Calculates the tax based on the provided amount using the configured tax rate.

        :param amount: The amount on which to calculate the tax (must be >= 0.0).
        :return: The tax as a float.
        :raises ValueError: If the amount is negative.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(amount, (float, int)):
            raise TypeError("Amount must be a number.")
        if amount < 0.0:
            raise ValueError(None)
        return amount * self.tax_rate

    def xǁOrderCalculatorǁcalculate_tax__mutmut_9(self, amount: float) -> float:
        """
        Calculates the tax based on the provided amount using the configured tax rate.

        :param amount: The amount on which to calculate the tax (must be >= 0.0).
        :return: The tax as a float.
        :raises ValueError: If the amount is negative.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(amount, (float, int)):
            raise TypeError("Amount must be a number.")
        if amount < 0.0:
            raise ValueError("XXCannot calculate tax on negative amount.XX")
        return amount * self.tax_rate

    def xǁOrderCalculatorǁcalculate_tax__mutmut_10(self, amount: float) -> float:
        """
        Calculates the tax based on the provided amount using the configured tax rate.

        :param amount: The amount on which to calculate the tax (must be >= 0.0).
        :return: The tax as a float.
        :raises ValueError: If the amount is negative.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(amount, (float, int)):
            raise TypeError("Amount must be a number.")
        if amount < 0.0:
            raise ValueError("cannot calculate tax on negative amount.")
        return amount * self.tax_rate

    def xǁOrderCalculatorǁcalculate_tax__mutmut_11(self, amount: float) -> float:
        """
        Calculates the tax based on the provided amount using the configured tax rate.

        :param amount: The amount on which to calculate the tax (must be >= 0.0).
        :return: The tax as a float.
        :raises ValueError: If the amount is negative.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(amount, (float, int)):
            raise TypeError("Amount must be a number.")
        if amount < 0.0:
            raise ValueError("CANNOT CALCULATE TAX ON NEGATIVE AMOUNT.")
        return amount * self.tax_rate

    def xǁOrderCalculatorǁcalculate_tax__mutmut_12(self, amount: float) -> float:
        """
        Calculates the tax based on the provided amount using the configured tax rate.

        :param amount: The amount on which to calculate the tax (must be >= 0.0).
        :return: The tax as a float.
        :raises ValueError: If the amount is negative.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(amount, (float, int)):
            raise TypeError("Amount must be a number.")
        if amount < 0.0:
            raise ValueError("Cannot calculate tax on negative amount.")
        return amount / self.tax_rate
    
    xǁOrderCalculatorǁcalculate_tax__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOrderCalculatorǁcalculate_tax__mutmut_1': xǁOrderCalculatorǁcalculate_tax__mutmut_1, 
        'xǁOrderCalculatorǁcalculate_tax__mutmut_2': xǁOrderCalculatorǁcalculate_tax__mutmut_2, 
        'xǁOrderCalculatorǁcalculate_tax__mutmut_3': xǁOrderCalculatorǁcalculate_tax__mutmut_3, 
        'xǁOrderCalculatorǁcalculate_tax__mutmut_4': xǁOrderCalculatorǁcalculate_tax__mutmut_4, 
        'xǁOrderCalculatorǁcalculate_tax__mutmut_5': xǁOrderCalculatorǁcalculate_tax__mutmut_5, 
        'xǁOrderCalculatorǁcalculate_tax__mutmut_6': xǁOrderCalculatorǁcalculate_tax__mutmut_6, 
        'xǁOrderCalculatorǁcalculate_tax__mutmut_7': xǁOrderCalculatorǁcalculate_tax__mutmut_7, 
        'xǁOrderCalculatorǁcalculate_tax__mutmut_8': xǁOrderCalculatorǁcalculate_tax__mutmut_8, 
        'xǁOrderCalculatorǁcalculate_tax__mutmut_9': xǁOrderCalculatorǁcalculate_tax__mutmut_9, 
        'xǁOrderCalculatorǁcalculate_tax__mutmut_10': xǁOrderCalculatorǁcalculate_tax__mutmut_10, 
        'xǁOrderCalculatorǁcalculate_tax__mutmut_11': xǁOrderCalculatorǁcalculate_tax__mutmut_11, 
        'xǁOrderCalculatorǁcalculate_tax__mutmut_12': xǁOrderCalculatorǁcalculate_tax__mutmut_12
    }
    
    def calculate_tax(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOrderCalculatorǁcalculate_tax__mutmut_orig"), object.__getattribute__(self, "xǁOrderCalculatorǁcalculate_tax__mutmut_mutants"), args, kwargs, self)
        return result 
    
    calculate_tax.__signature__ = _mutmut_signature(xǁOrderCalculatorǁcalculate_tax__mutmut_orig)
    xǁOrderCalculatorǁcalculate_tax__mutmut_orig.__name__ = 'xǁOrderCalculatorǁcalculate_tax'

    def xǁOrderCalculatorǁcalculate_total__mutmut_orig(self, discount: float = 0.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.

        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.

        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")

        subtotal = self.get_subtotal()
        if subtotal < 0.0:
            raise ValueError("Cannot calculate total on negative subtotal.")
        discounted_subtotal = self.apply_discount(subtotal, discount)
        shipping_cost = self.calculate_shipping(discounted_subtotal)
        tax = self.calculate_tax(discounted_subtotal + shipping_cost)
        return discounted_subtotal + shipping_cost + tax

    def xǁOrderCalculatorǁcalculate_total__mutmut_1(self, discount: float = 1.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.

        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.

        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")

        subtotal = self.get_subtotal()
        if subtotal < 0.0:
            raise ValueError("Cannot calculate total on negative subtotal.")
        discounted_subtotal = self.apply_discount(subtotal, discount)
        shipping_cost = self.calculate_shipping(discounted_subtotal)
        tax = self.calculate_tax(discounted_subtotal + shipping_cost)
        return discounted_subtotal + shipping_cost + tax

    def xǁOrderCalculatorǁcalculate_total__mutmut_2(self, discount: float = 0.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.

        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.

        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        if isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")

        subtotal = self.get_subtotal()
        if subtotal < 0.0:
            raise ValueError("Cannot calculate total on negative subtotal.")
        discounted_subtotal = self.apply_discount(subtotal, discount)
        shipping_cost = self.calculate_shipping(discounted_subtotal)
        tax = self.calculate_tax(discounted_subtotal + shipping_cost)
        return discounted_subtotal + shipping_cost + tax

    def xǁOrderCalculatorǁcalculate_total__mutmut_3(self, discount: float = 0.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.

        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.

        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discount, (float, int)):
            raise TypeError(None)

        subtotal = self.get_subtotal()
        if subtotal < 0.0:
            raise ValueError("Cannot calculate total on negative subtotal.")
        discounted_subtotal = self.apply_discount(subtotal, discount)
        shipping_cost = self.calculate_shipping(discounted_subtotal)
        tax = self.calculate_tax(discounted_subtotal + shipping_cost)
        return discounted_subtotal + shipping_cost + tax

    def xǁOrderCalculatorǁcalculate_total__mutmut_4(self, discount: float = 0.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.

        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.

        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discount, (float, int)):
            raise TypeError("XXDiscount must be a number.XX")

        subtotal = self.get_subtotal()
        if subtotal < 0.0:
            raise ValueError("Cannot calculate total on negative subtotal.")
        discounted_subtotal = self.apply_discount(subtotal, discount)
        shipping_cost = self.calculate_shipping(discounted_subtotal)
        tax = self.calculate_tax(discounted_subtotal + shipping_cost)
        return discounted_subtotal + shipping_cost + tax

    def xǁOrderCalculatorǁcalculate_total__mutmut_5(self, discount: float = 0.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.

        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.

        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discount, (float, int)):
            raise TypeError("discount must be a number.")

        subtotal = self.get_subtotal()
        if subtotal < 0.0:
            raise ValueError("Cannot calculate total on negative subtotal.")
        discounted_subtotal = self.apply_discount(subtotal, discount)
        shipping_cost = self.calculate_shipping(discounted_subtotal)
        tax = self.calculate_tax(discounted_subtotal + shipping_cost)
        return discounted_subtotal + shipping_cost + tax

    def xǁOrderCalculatorǁcalculate_total__mutmut_6(self, discount: float = 0.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.

        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.

        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discount, (float, int)):
            raise TypeError("DISCOUNT MUST BE A NUMBER.")

        subtotal = self.get_subtotal()
        if subtotal < 0.0:
            raise ValueError("Cannot calculate total on negative subtotal.")
        discounted_subtotal = self.apply_discount(subtotal, discount)
        shipping_cost = self.calculate_shipping(discounted_subtotal)
        tax = self.calculate_tax(discounted_subtotal + shipping_cost)
        return discounted_subtotal + shipping_cost + tax

    def xǁOrderCalculatorǁcalculate_total__mutmut_7(self, discount: float = 0.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.

        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.

        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")

        subtotal = None
        if subtotal < 0.0:
            raise ValueError("Cannot calculate total on negative subtotal.")
        discounted_subtotal = self.apply_discount(subtotal, discount)
        shipping_cost = self.calculate_shipping(discounted_subtotal)
        tax = self.calculate_tax(discounted_subtotal + shipping_cost)
        return discounted_subtotal + shipping_cost + tax

    def xǁOrderCalculatorǁcalculate_total__mutmut_8(self, discount: float = 0.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.

        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.

        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")

        subtotal = self.get_subtotal()
        if subtotal <= 0.0:
            raise ValueError("Cannot calculate total on negative subtotal.")
        discounted_subtotal = self.apply_discount(subtotal, discount)
        shipping_cost = self.calculate_shipping(discounted_subtotal)
        tax = self.calculate_tax(discounted_subtotal + shipping_cost)
        return discounted_subtotal + shipping_cost + tax

    def xǁOrderCalculatorǁcalculate_total__mutmut_9(self, discount: float = 0.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.

        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.

        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")

        subtotal = self.get_subtotal()
        if subtotal < 1.0:
            raise ValueError("Cannot calculate total on negative subtotal.")
        discounted_subtotal = self.apply_discount(subtotal, discount)
        shipping_cost = self.calculate_shipping(discounted_subtotal)
        tax = self.calculate_tax(discounted_subtotal + shipping_cost)
        return discounted_subtotal + shipping_cost + tax

    def xǁOrderCalculatorǁcalculate_total__mutmut_10(self, discount: float = 0.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.

        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.

        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")

        subtotal = self.get_subtotal()
        if subtotal < 0.0:
            raise ValueError(None)
        discounted_subtotal = self.apply_discount(subtotal, discount)
        shipping_cost = self.calculate_shipping(discounted_subtotal)
        tax = self.calculate_tax(discounted_subtotal + shipping_cost)
        return discounted_subtotal + shipping_cost + tax

    def xǁOrderCalculatorǁcalculate_total__mutmut_11(self, discount: float = 0.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.

        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.

        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")

        subtotal = self.get_subtotal()
        if subtotal < 0.0:
            raise ValueError("XXCannot calculate total on negative subtotal.XX")
        discounted_subtotal = self.apply_discount(subtotal, discount)
        shipping_cost = self.calculate_shipping(discounted_subtotal)
        tax = self.calculate_tax(discounted_subtotal + shipping_cost)
        return discounted_subtotal + shipping_cost + tax

    def xǁOrderCalculatorǁcalculate_total__mutmut_12(self, discount: float = 0.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.

        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.

        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")

        subtotal = self.get_subtotal()
        if subtotal < 0.0:
            raise ValueError("cannot calculate total on negative subtotal.")
        discounted_subtotal = self.apply_discount(subtotal, discount)
        shipping_cost = self.calculate_shipping(discounted_subtotal)
        tax = self.calculate_tax(discounted_subtotal + shipping_cost)
        return discounted_subtotal + shipping_cost + tax

    def xǁOrderCalculatorǁcalculate_total__mutmut_13(self, discount: float = 0.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.

        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.

        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")

        subtotal = self.get_subtotal()
        if subtotal < 0.0:
            raise ValueError("CANNOT CALCULATE TOTAL ON NEGATIVE SUBTOTAL.")
        discounted_subtotal = self.apply_discount(subtotal, discount)
        shipping_cost = self.calculate_shipping(discounted_subtotal)
        tax = self.calculate_tax(discounted_subtotal + shipping_cost)
        return discounted_subtotal + shipping_cost + tax

    def xǁOrderCalculatorǁcalculate_total__mutmut_14(self, discount: float = 0.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.

        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.

        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")

        subtotal = self.get_subtotal()
        if subtotal < 0.0:
            raise ValueError("Cannot calculate total on negative subtotal.")
        discounted_subtotal = None
        shipping_cost = self.calculate_shipping(discounted_subtotal)
        tax = self.calculate_tax(discounted_subtotal + shipping_cost)
        return discounted_subtotal + shipping_cost + tax

    def xǁOrderCalculatorǁcalculate_total__mutmut_15(self, discount: float = 0.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.

        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.

        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")

        subtotal = self.get_subtotal()
        if subtotal < 0.0:
            raise ValueError("Cannot calculate total on negative subtotal.")
        discounted_subtotal = self.apply_discount(None, discount)
        shipping_cost = self.calculate_shipping(discounted_subtotal)
        tax = self.calculate_tax(discounted_subtotal + shipping_cost)
        return discounted_subtotal + shipping_cost + tax

    def xǁOrderCalculatorǁcalculate_total__mutmut_16(self, discount: float = 0.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.

        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.

        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")

        subtotal = self.get_subtotal()
        if subtotal < 0.0:
            raise ValueError("Cannot calculate total on negative subtotal.")
        discounted_subtotal = self.apply_discount(subtotal, None)
        shipping_cost = self.calculate_shipping(discounted_subtotal)
        tax = self.calculate_tax(discounted_subtotal + shipping_cost)
        return discounted_subtotal + shipping_cost + tax

    def xǁOrderCalculatorǁcalculate_total__mutmut_17(self, discount: float = 0.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.

        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.

        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")

        subtotal = self.get_subtotal()
        if subtotal < 0.0:
            raise ValueError("Cannot calculate total on negative subtotal.")
        discounted_subtotal = self.apply_discount(discount)
        shipping_cost = self.calculate_shipping(discounted_subtotal)
        tax = self.calculate_tax(discounted_subtotal + shipping_cost)
        return discounted_subtotal + shipping_cost + tax

    def xǁOrderCalculatorǁcalculate_total__mutmut_18(self, discount: float = 0.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.

        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.

        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")

        subtotal = self.get_subtotal()
        if subtotal < 0.0:
            raise ValueError("Cannot calculate total on negative subtotal.")
        discounted_subtotal = self.apply_discount(subtotal, )
        shipping_cost = self.calculate_shipping(discounted_subtotal)
        tax = self.calculate_tax(discounted_subtotal + shipping_cost)
        return discounted_subtotal + shipping_cost + tax

    def xǁOrderCalculatorǁcalculate_total__mutmut_19(self, discount: float = 0.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.

        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.

        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")

        subtotal = self.get_subtotal()
        if subtotal < 0.0:
            raise ValueError("Cannot calculate total on negative subtotal.")
        discounted_subtotal = self.apply_discount(subtotal, discount)
        shipping_cost = None
        tax = self.calculate_tax(discounted_subtotal + shipping_cost)
        return discounted_subtotal + shipping_cost + tax

    def xǁOrderCalculatorǁcalculate_total__mutmut_20(self, discount: float = 0.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.

        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.

        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")

        subtotal = self.get_subtotal()
        if subtotal < 0.0:
            raise ValueError("Cannot calculate total on negative subtotal.")
        discounted_subtotal = self.apply_discount(subtotal, discount)
        shipping_cost = self.calculate_shipping(None)
        tax = self.calculate_tax(discounted_subtotal + shipping_cost)
        return discounted_subtotal + shipping_cost + tax

    def xǁOrderCalculatorǁcalculate_total__mutmut_21(self, discount: float = 0.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.

        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.

        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")

        subtotal = self.get_subtotal()
        if subtotal < 0.0:
            raise ValueError("Cannot calculate total on negative subtotal.")
        discounted_subtotal = self.apply_discount(subtotal, discount)
        shipping_cost = self.calculate_shipping(discounted_subtotal)
        tax = None
        return discounted_subtotal + shipping_cost + tax

    def xǁOrderCalculatorǁcalculate_total__mutmut_22(self, discount: float = 0.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.

        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.

        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")

        subtotal = self.get_subtotal()
        if subtotal < 0.0:
            raise ValueError("Cannot calculate total on negative subtotal.")
        discounted_subtotal = self.apply_discount(subtotal, discount)
        shipping_cost = self.calculate_shipping(discounted_subtotal)
        tax = self.calculate_tax(None)
        return discounted_subtotal + shipping_cost + tax

    def xǁOrderCalculatorǁcalculate_total__mutmut_23(self, discount: float = 0.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.

        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.

        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")

        subtotal = self.get_subtotal()
        if subtotal < 0.0:
            raise ValueError("Cannot calculate total on negative subtotal.")
        discounted_subtotal = self.apply_discount(subtotal, discount)
        shipping_cost = self.calculate_shipping(discounted_subtotal)
        tax = self.calculate_tax(discounted_subtotal - shipping_cost)
        return discounted_subtotal + shipping_cost + tax

    def xǁOrderCalculatorǁcalculate_total__mutmut_24(self, discount: float = 0.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.

        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.

        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")

        subtotal = self.get_subtotal()
        if subtotal < 0.0:
            raise ValueError("Cannot calculate total on negative subtotal.")
        discounted_subtotal = self.apply_discount(subtotal, discount)
        shipping_cost = self.calculate_shipping(discounted_subtotal)
        tax = self.calculate_tax(discounted_subtotal + shipping_cost)
        return discounted_subtotal - shipping_cost + tax

    def xǁOrderCalculatorǁcalculate_total__mutmut_25(self, discount: float = 0.0) -> float:
        """
        Calculates the total cost of the order after applying discount, shipping, and tax.

        This method performs the following steps:
        1. Calculates the subtotal from all items.
        2. Applies the given discount.
        3. Adds shipping cost if necessary.
        4. Calculates tax on the discounted subtotal + shipping.

        :param discount: Discount rate between 0.0 and 1.0 (e.g. 0.2 = 20%).
        :return: The final total as a float.
        :raises ValueError:
            - If the subtotal is negative.
            - If the discount is invalid.
            - If the order is empty.
        :raises TypeError: If input is not a number.
        """
        if not isinstance(discount, (float, int)):
            raise TypeError("Discount must be a number.")

        subtotal = self.get_subtotal()
        if subtotal < 0.0:
            raise ValueError("Cannot calculate total on negative subtotal.")
        discounted_subtotal = self.apply_discount(subtotal, discount)
        shipping_cost = self.calculate_shipping(discounted_subtotal)
        tax = self.calculate_tax(discounted_subtotal + shipping_cost)
        return discounted_subtotal + shipping_cost - tax
    
    xǁOrderCalculatorǁcalculate_total__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOrderCalculatorǁcalculate_total__mutmut_1': xǁOrderCalculatorǁcalculate_total__mutmut_1, 
        'xǁOrderCalculatorǁcalculate_total__mutmut_2': xǁOrderCalculatorǁcalculate_total__mutmut_2, 
        'xǁOrderCalculatorǁcalculate_total__mutmut_3': xǁOrderCalculatorǁcalculate_total__mutmut_3, 
        'xǁOrderCalculatorǁcalculate_total__mutmut_4': xǁOrderCalculatorǁcalculate_total__mutmut_4, 
        'xǁOrderCalculatorǁcalculate_total__mutmut_5': xǁOrderCalculatorǁcalculate_total__mutmut_5, 
        'xǁOrderCalculatorǁcalculate_total__mutmut_6': xǁOrderCalculatorǁcalculate_total__mutmut_6, 
        'xǁOrderCalculatorǁcalculate_total__mutmut_7': xǁOrderCalculatorǁcalculate_total__mutmut_7, 
        'xǁOrderCalculatorǁcalculate_total__mutmut_8': xǁOrderCalculatorǁcalculate_total__mutmut_8, 
        'xǁOrderCalculatorǁcalculate_total__mutmut_9': xǁOrderCalculatorǁcalculate_total__mutmut_9, 
        'xǁOrderCalculatorǁcalculate_total__mutmut_10': xǁOrderCalculatorǁcalculate_total__mutmut_10, 
        'xǁOrderCalculatorǁcalculate_total__mutmut_11': xǁOrderCalculatorǁcalculate_total__mutmut_11, 
        'xǁOrderCalculatorǁcalculate_total__mutmut_12': xǁOrderCalculatorǁcalculate_total__mutmut_12, 
        'xǁOrderCalculatorǁcalculate_total__mutmut_13': xǁOrderCalculatorǁcalculate_total__mutmut_13, 
        'xǁOrderCalculatorǁcalculate_total__mutmut_14': xǁOrderCalculatorǁcalculate_total__mutmut_14, 
        'xǁOrderCalculatorǁcalculate_total__mutmut_15': xǁOrderCalculatorǁcalculate_total__mutmut_15, 
        'xǁOrderCalculatorǁcalculate_total__mutmut_16': xǁOrderCalculatorǁcalculate_total__mutmut_16, 
        'xǁOrderCalculatorǁcalculate_total__mutmut_17': xǁOrderCalculatorǁcalculate_total__mutmut_17, 
        'xǁOrderCalculatorǁcalculate_total__mutmut_18': xǁOrderCalculatorǁcalculate_total__mutmut_18, 
        'xǁOrderCalculatorǁcalculate_total__mutmut_19': xǁOrderCalculatorǁcalculate_total__mutmut_19, 
        'xǁOrderCalculatorǁcalculate_total__mutmut_20': xǁOrderCalculatorǁcalculate_total__mutmut_20, 
        'xǁOrderCalculatorǁcalculate_total__mutmut_21': xǁOrderCalculatorǁcalculate_total__mutmut_21, 
        'xǁOrderCalculatorǁcalculate_total__mutmut_22': xǁOrderCalculatorǁcalculate_total__mutmut_22, 
        'xǁOrderCalculatorǁcalculate_total__mutmut_23': xǁOrderCalculatorǁcalculate_total__mutmut_23, 
        'xǁOrderCalculatorǁcalculate_total__mutmut_24': xǁOrderCalculatorǁcalculate_total__mutmut_24, 
        'xǁOrderCalculatorǁcalculate_total__mutmut_25': xǁOrderCalculatorǁcalculate_total__mutmut_25
    }
    
    def calculate_total(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOrderCalculatorǁcalculate_total__mutmut_orig"), object.__getattribute__(self, "xǁOrderCalculatorǁcalculate_total__mutmut_mutants"), args, kwargs, self)
        return result 
    
    calculate_total.__signature__ = _mutmut_signature(xǁOrderCalculatorǁcalculate_total__mutmut_orig)
    xǁOrderCalculatorǁcalculate_total__mutmut_orig.__name__ = 'xǁOrderCalculatorǁcalculate_total'

    def xǁOrderCalculatorǁtotal_items__mutmut_orig(self) -> int:
        """
        Returns the total quantity of all items in the order.

        :return: The sum of the quantities of all items.
        :return:
        """
        return sum(item["quantity"] for item in self.items)

    def xǁOrderCalculatorǁtotal_items__mutmut_1(self) -> int:
        """
        Returns the total quantity of all items in the order.

        :return: The sum of the quantities of all items.
        :return:
        """
        return sum(None)

    def xǁOrderCalculatorǁtotal_items__mutmut_2(self) -> int:
        """
        Returns the total quantity of all items in the order.

        :return: The sum of the quantities of all items.
        :return:
        """
        return sum(item["XXquantityXX"] for item in self.items)

    def xǁOrderCalculatorǁtotal_items__mutmut_3(self) -> int:
        """
        Returns the total quantity of all items in the order.

        :return: The sum of the quantities of all items.
        :return:
        """
        return sum(item["QUANTITY"] for item in self.items)

    def xǁOrderCalculatorǁtotal_items__mutmut_4(self) -> int:
        """
        Returns the total quantity of all items in the order.

        :return: The sum of the quantities of all items.
        :return:
        """
        return sum(item["Quantity"] for item in self.items)
    
    xǁOrderCalculatorǁtotal_items__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOrderCalculatorǁtotal_items__mutmut_1': xǁOrderCalculatorǁtotal_items__mutmut_1, 
        'xǁOrderCalculatorǁtotal_items__mutmut_2': xǁOrderCalculatorǁtotal_items__mutmut_2, 
        'xǁOrderCalculatorǁtotal_items__mutmut_3': xǁOrderCalculatorǁtotal_items__mutmut_3, 
        'xǁOrderCalculatorǁtotal_items__mutmut_4': xǁOrderCalculatorǁtotal_items__mutmut_4
    }
    
    def total_items(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOrderCalculatorǁtotal_items__mutmut_orig"), object.__getattribute__(self, "xǁOrderCalculatorǁtotal_items__mutmut_mutants"), args, kwargs, self)
        return result 
    
    total_items.__signature__ = _mutmut_signature(xǁOrderCalculatorǁtotal_items__mutmut_orig)
    xǁOrderCalculatorǁtotal_items__mutmut_orig.__name__ = 'xǁOrderCalculatorǁtotal_items'

    def xǁOrderCalculatorǁclear_order__mutmut_orig(self):
        """
        Removes all items from the order, resetting it to an empty state.
        """
        self.items = []

    def xǁOrderCalculatorǁclear_order__mutmut_1(self):
        """
        Removes all items from the order, resetting it to an empty state.
        """
        self.items = None
    
    xǁOrderCalculatorǁclear_order__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOrderCalculatorǁclear_order__mutmut_1': xǁOrderCalculatorǁclear_order__mutmut_1
    }
    
    def clear_order(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOrderCalculatorǁclear_order__mutmut_orig"), object.__getattribute__(self, "xǁOrderCalculatorǁclear_order__mutmut_mutants"), args, kwargs, self)
        return result 
    
    clear_order.__signature__ = _mutmut_signature(xǁOrderCalculatorǁclear_order__mutmut_orig)
    xǁOrderCalculatorǁclear_order__mutmut_orig.__name__ = 'xǁOrderCalculatorǁclear_order'

    def xǁOrderCalculatorǁlist_items__mutmut_orig(self) -> List[str]:
        """
        Returns a list of all unique item names currently in the order.

        :return: A list of unique item names (no duplicates).
        """
        return list(set(item["name"] for item in self.items))

    def xǁOrderCalculatorǁlist_items__mutmut_1(self) -> List[str]:
        """
        Returns a list of all unique item names currently in the order.

        :return: A list of unique item names (no duplicates).
        """
        return list(None)

    def xǁOrderCalculatorǁlist_items__mutmut_2(self) -> List[str]:
        """
        Returns a list of all unique item names currently in the order.

        :return: A list of unique item names (no duplicates).
        """
        return list(set(None))

    def xǁOrderCalculatorǁlist_items__mutmut_3(self) -> List[str]:
        """
        Returns a list of all unique item names currently in the order.

        :return: A list of unique item names (no duplicates).
        """
        return list(set(item["XXnameXX"] for item in self.items))

    def xǁOrderCalculatorǁlist_items__mutmut_4(self) -> List[str]:
        """
        Returns a list of all unique item names currently in the order.

        :return: A list of unique item names (no duplicates).
        """
        return list(set(item["NAME"] for item in self.items))

    def xǁOrderCalculatorǁlist_items__mutmut_5(self) -> List[str]:
        """
        Returns a list of all unique item names currently in the order.

        :return: A list of unique item names (no duplicates).
        """
        return list(set(item["Name"] for item in self.items))
    
    xǁOrderCalculatorǁlist_items__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOrderCalculatorǁlist_items__mutmut_1': xǁOrderCalculatorǁlist_items__mutmut_1, 
        'xǁOrderCalculatorǁlist_items__mutmut_2': xǁOrderCalculatorǁlist_items__mutmut_2, 
        'xǁOrderCalculatorǁlist_items__mutmut_3': xǁOrderCalculatorǁlist_items__mutmut_3, 
        'xǁOrderCalculatorǁlist_items__mutmut_4': xǁOrderCalculatorǁlist_items__mutmut_4, 
        'xǁOrderCalculatorǁlist_items__mutmut_5': xǁOrderCalculatorǁlist_items__mutmut_5
    }
    
    def list_items(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOrderCalculatorǁlist_items__mutmut_orig"), object.__getattribute__(self, "xǁOrderCalculatorǁlist_items__mutmut_mutants"), args, kwargs, self)
        return result 
    
    list_items.__signature__ = _mutmut_signature(xǁOrderCalculatorǁlist_items__mutmut_orig)
    xǁOrderCalculatorǁlist_items__mutmut_orig.__name__ = 'xǁOrderCalculatorǁlist_items'

    def xǁOrderCalculatorǁis_empty__mutmut_orig(self) -> bool:
        """
        Checks whether the order is currently empty.

        :return: True if no items are in the order, False otherwise.
        """
        return len(self.items) == 0

    def xǁOrderCalculatorǁis_empty__mutmut_1(self) -> bool:
        """
        Checks whether the order is currently empty.

        :return: True if no items are in the order, False otherwise.
        """
        return len(self.items) != 0

    def xǁOrderCalculatorǁis_empty__mutmut_2(self) -> bool:
        """
        Checks whether the order is currently empty.

        :return: True if no items are in the order, False otherwise.
        """
        return len(self.items) == 1
    
    xǁOrderCalculatorǁis_empty__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁOrderCalculatorǁis_empty__mutmut_1': xǁOrderCalculatorǁis_empty__mutmut_1, 
        'xǁOrderCalculatorǁis_empty__mutmut_2': xǁOrderCalculatorǁis_empty__mutmut_2
    }
    
    def is_empty(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁOrderCalculatorǁis_empty__mutmut_orig"), object.__getattribute__(self, "xǁOrderCalculatorǁis_empty__mutmut_mutants"), args, kwargs, self)
        return result 
    
    is_empty.__signature__ = _mutmut_signature(xǁOrderCalculatorǁis_empty__mutmut_orig)
    xǁOrderCalculatorǁis_empty__mutmut_orig.__name__ = 'xǁOrderCalculatorǁis_empty'