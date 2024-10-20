class ArithmeticCoding:
    def __init__(self, message):
        self.message = message
        self.intervals = {}
        self._calculate_probabilities(message)
        self._create_intervals()

    def _calculate_probabilities(self, message):
        """Calculates the probability of each symbol in the message."""
        freq = {}
        for symbol in message:
            freq[symbol] = freq.get(symbol, 0) + 1

        total_symbols = len(message)
        self.probabilities = {symbol: count / total_symbols for symbol, count in freq.items()}

    def _create_intervals(self):
        """Creates cumulative probability intervals for each symbol."""
        low = 0.0
        for symbol, prob in self.probabilities.items():
            high = low + prob
            self.intervals[symbol] = (low, high)
            low = high

    def encode(self, print_probabilities=False):
        """Encodes a message into an interval."""
        low, high = 0.0, 1.0
        for symbol in self.message:
            symbol_low, symbol_high = self.intervals[symbol]
            range_ = high - low
            high = low + range_ * symbol_high
            low = low + range_ * symbol_low

        if print_probabilities:
            print('message:', self.message)
            print('probabilities:', self.probabilities)

        # The final encoding is any number in the range (low, high)
        return (low + high) / 2

    def decode(self, encoded_value, message_length):
        """Decodes an encoded value back into the original message."""
        low, high = 0.0, 1.0
        decoded_message = []

        for _ in range(message_length):
            value_range = high - low
            normalized_value = (encoded_value - low) / value_range
            for symbol, (symbol_low, symbol_high) in self.intervals.items():
                if symbol_low <= normalized_value < symbol_high:
                    decoded_message.append(symbol)
                    high = low + value_range * symbol_high
                    low = low + value_range * symbol_low
                    break

        return ''.join(decoded_message)


# Example usage:
if __name__ == "__main__":

    message = "abac"
    arithmetic_coder = ArithmeticCoding(message)
    encoded_value = arithmetic_coder.encode(print_probabilities=True)
    print(f"Encoded value: {encoded_value}")

    decoded_message = arithmetic_coder.decode(encoded_value, len(message))
    print(f"Decoded message: {decoded_message}")
