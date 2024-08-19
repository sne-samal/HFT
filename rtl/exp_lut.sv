// lut of 1 million entries, -1 to 1 
// fixed-point numbers - 32 integer bits, 32 fractional bits (q32.32)

module exp_lut #
(
    parameter array_size = 1_000_000
)
(
    input logic i_clk,
    input logic [63:0] input_value, // q32.32 fixed-point input
    output logic [63:0] exp_value // Scaled exponential value output
);
    
    logic [63:0] lut [array_size-1:0];
    logic [31:0] temp;
    logic signed [127:0] scaled_value;
    // Read the exponential values from the memory file
    initial begin
        $readmemh("/home/ronit/HFT/HFT/rtl/exp_values.mem", lut);
    end
    // Calculate the index based on the input_value
    logic [19:0] index; // 20-bit index to cover array_size (log2(1000000) = ~20 bits)
    always_comb begin
        temp = input_value[63:32];
            // Scale and clamp the input_value to the range of indices
            if (temp == 32'h00000003) begin// -1.0 in q32.32
                index = 0;
            end
            else if (temp == 32'h00000001) begin

                index = array_size - 1;
            end
            else begin 
                scaled_value = (input_value + 64'h0000000100000000) * (array_size-1) * 0.5;
                index = scaled_value[63:32]; // Division by 2^32 and truncation to 20 bits    
            end

    end

    // Lookup the exponential value
    assign exp_value = lut[index];

endmodule
