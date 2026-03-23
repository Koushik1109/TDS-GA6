from hypothesis import given, strategies as st

# We assume compute_ticket_revenue is injected/available in the execution environment.
# If it needs to be imported, you would add the import statement here.

@given(
    price=st.integers(min_value=0, max_value=10**10), 
    quantity=st.integers(min_value=0, max_value=10**10)
)
def test_property(price, quantity):
    """
    Property: The computed ticket revenue should exactly match 
    the mathematical product of price and quantity, with no integer overflow.
    """
    expected_revenue = price * quantity
    assert compute_ticket_revenue(price, quantity) == expected_revenue
