from langchain.tools import tool
from langchain_classic.agents import tool
from langchain_community.utilities import WikipediaAPIWrapper


@tool
def add_numbers(
    numbers: list[float],
    use_absolute: bool = False,
) -> float:
    """Add all numbers in the provided list."""

    if use_absolute:
        numbers = [abs(number) for number in numbers]

    return sum(numbers)

@tool
def subtract_numbers(
    numbers: list[float],
    use_absolute: bool = False,
) -> float:
    """Subtract all numbers in the provided list."""

    if use_absolute:
        numbers = [abs(number) for number in numbers]
    if not numbers:
        return {"result": 0}

    result = numbers[0]
    for number in numbers[1:]:
        result -= number

    return result
@tool
def multiply_numbers(
    numbers: list[float],
    use_absolute: bool = False,
) -> float:
    """Multiply all numbers in the provided list."""

    if use_absolute:
        numbers = [abs(number) for number in numbers]

    result = 1
    for number in numbers:
        result *= number

    return result

@tool
def divide_numbers(
    numbers: list[float],
    use_absolute: bool = False,
) -> float:
    """Divide all numbers in the provided list."""

    if use_absolute:
        numbers = [abs(number) for number in numbers]

    result = numbers[0]
    for number in numbers[1:]:
        if number == 0:
            raise ValueError("Cannot divide by zero.")
        result /= number

    return result
@tool
def search_wikipedia(query: str) -> str:
    """Search Wikipedia for factual information about a topic.
    
    Parameters:
    - query (str): The topic or question to search for on Wikipedia
    
    Returns:
    - str: A summary of relevant information from Wikipedia
    """
    wiki = WikipediaAPIWrapper()
    return wiki.run(query)