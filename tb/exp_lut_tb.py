import cocotb
import random
import math
from cocotb.triggers import Timer, RisingEdge
from cocotb.clock import Clock
from helpers import make_fixed_point_input, convert_fixed_point_output
# Define a list of input values for testing
test_values = [0.30349, 0.5, 1.0, 0.3, 0.123456, 0.99839, 0.48548, 0.826813]

@cocotb.test()
async def parameterized_fixed_input_test(dut):
    """Parameterized Fixed input testing"""

    # Start the clock
    cocotb.start_soon(Clock(dut.i_clk, 10, "ns").start())

    for test_value in test_values:
        # Initialize input value
        dut.input_value.value = 0  # Start with 0 or a known state
        dut.exp_value.value = 0

        await RisingEdge(dut.i_clk)
        
        # Apply the input
        dut.input_value.value = make_fixed_point_input(test_value)
        
        # Wait for a few clock cycles for the DUT to process the input
        await RisingEdge(dut.i_clk)
        await RisingEdge(dut.i_clk)

        # Capture and convert the output
        output = convert_fixed_point_output(dut.exp_value.value)
        dut._log.info(f"Input: {test_value} => ExpValue: {output}")

        # Optionally, check the output against the expected value
        expected_output = math.exp(test_value)
        tolerance = 0.00001 * expected_output  # Adjust tolerance as needed
        assert abs(output - expected_output) < tolerance, \
            f"Expected {expected_output}, got {output}"

        # Additional clock cycles to observe any delayed responses
        await RisingEdge(dut.i_clk)

# Define a list of input values for testing
test_values_neg = [-0.30349, -0.5, -1.0, -0.3, -0.123456, -0.99839, -0.48548, -0.826813]

@cocotb.test()
async def multi_neg_test(dut):
    """Parameterized Fixed input testing"""

    # Start the clock
    cocotb.start_soon(Clock(dut.i_clk, 10, "ns").start())

    for test_value in test_values_neg:
        # Initialize input value
        dut.input_value.value = 0  # Start with 0 or a known state
        dut.exp_value.value = 0

        await RisingEdge(dut.i_clk)
        
        # Apply the input
        dut.input_value.value = make_fixed_point_input(test_value)
        
        # Wait for a few clock cycles for the DUT to process the input
        await RisingEdge(dut.i_clk)
        await RisingEdge(dut.i_clk)

        # Capture and convert the output
        output = convert_fixed_point_output(dut.exp_value.value)
        dut._log.info(f"Input: {test_value} => ExpValue: {output}")

        # Optionally, check the output against the expected value
        expected_output = math.exp(test_value)
        tolerance = 0.00001 * expected_output  # Adjust tolerance as needed
        assert abs(output - expected_output) < tolerance, \
            f"Expected {expected_output}, got {output}"

        # Additional clock cycles to observe any delayed responses
        await RisingEdge(dut.i_clk)


# positive limit testing
@cocotb.test()
async def pos_limit(dut):
    """Fixed input testing"""

    # Start the clock
    cocotb.start_soon(Clock(dut.i_clk, 10, "ns").start())

    # Initialize input value
    dut.input_value.value = 0  # Start with 0 or a known state
    dut.exp_value.value = 0

    await RisingEdge(dut.i_clk)
    await RisingEdge(dut.i_clk)
    # Reset the DUT if applicable
    # dut.i_rst <= 1
    # await Timer(10, units="ns")
    # dut.i_rst <= 0

    # Apply the input
    test_value = 1.02845
    dut.input_value.value = make_fixed_point_input(test_value)
    
    # Wait for a few clock cycles for the DUT to process the input
    await RisingEdge(dut.i_clk)
    await RisingEdge(dut.i_clk)

    # Capture and convert the output
    output = convert_fixed_point_output(dut.exp_value.value)
    dut._log.info(f"Input: {test_value} => ExpValue: {output}")

    # Optionally, check the output against the expected value
    expected_output = 2.7182799999136478
    tolerance = 0.00001 * expected_output  # Adjust tolerance as needed
    assert abs(output - expected_output) < tolerance, \
        f"Expected {expected_output}, got {output}"

    # Additional clock cycles to observe any delayed responses
    await RisingEdge(dut.i_clk)

# negative limit testing
@cocotb.test()
async def neg_limit(dut):
    """Fixed input testing"""

    # Start the clock
    cocotb.start_soon(Clock(dut.i_clk, 10, "ns").start())

    # Initialize input value
    dut.input_value.value = 0  # Start with 0 or a known state
    dut.exp_value.value = 0

    await RisingEdge(dut.i_clk)
    # Reset the DUT if applicable
    # dut.i_rst <= 1
    # await Timer(10, units="ns")
    # dut.i_rst <= 0

    # Apply the input
    test_value = -1.483
    dut.input_value.value = make_fixed_point_input(test_value)
    
    # Wait for a few clock cycles for the DUT to process the input
    await RisingEdge(dut.i_clk)
    await RisingEdge(dut.i_clk)

    # Capture and convert the output
    output = convert_fixed_point_output(dut.exp_value.value)
    dut._log.info(f"Input: {make_fixed_point_input(test_value)} => ExpValue: {output}")

    # Optionally, check the output against the expected value
    expected_output = 0.367879
    tolerance = 0.00001 * expected_output  # Adjust tolerance as needed
    assert abs(output - expected_output) < tolerance, \
        f"Expected {expected_output}, got {output}"

    # Additional clock cycles to observe any delayed responses
    await RisingEdge(dut.i_clk)
