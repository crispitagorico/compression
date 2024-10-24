# Huffman Coding

Huffman coding is an example of **prefix codes**, which is a special type of symbol codes. Namely, symbol codes assign codewords to indvidual symbols. Prefix codes are codes in which no codeword is a prefix to another codeword. This can effectively prevent the possible errors occuring in the decoding process. The encoder creates a dictionary that associates each symbol with a binary representation and replaces each symbol of the original data with the corresponding representation. The decoder simply inverts the above process.

The main goal is to achieve lossless compression and shortest average length of binary codes.

Huffman codes satisfy the following two properties:
Property 1: huffman tree assigns shorter binary codes to more frequent symbols, and longer ones to less frequent symbols
Property 2: the two symbols that occur least frequently will have the same length, and their binary codes only differ in the last bit

It is obvious to see why property 1 holds.
The first half of property 2 is less trivial to show. Suppose an optimum code C exists in which the two codewords corresponding to the two least probable symbols do not have the same length. Suppose the longer codeword is k bits longer than the shorter codeword. Because this is a prefix code, the shorter codeword cannot be a prefix of the longer codeword. This means that even if we drop the last k bits of the longer codeword, the two codewords would still be distinct. As these codewords correspond to the least probable symbols in the alphabet, no other codeword can be longer than these codewords; therefore, there is no danger that the shortened codeword would become the prefix of some other codeword. Furthermore, by dropping these k bits we obtain a new code that has a shorter average length than C. But this violates our initial contention that C is an optimal code.[1] The second half of property 2 is just the defining characteristics of huffman codes.

1.	Sayood K. Introduction to data compression. The Morgan Kaufmann series in multimedia information and systems. Elsevier Science & Technology; 2006.
 	 
# Arithmetic Coding

Arithmetic coding, also known as range coding, is an example of **streaming codes**. Unlike symbol codes, streaming codes assign codewords to entire messages rather than individual symbols. 

The core idea is to associate each symbol with a **subinterval** of the interval $$[0,1]$$, where the length of the subinterval corresponds to the symbol's probability. When encoding a sequence, subsequent symbols are represented as subintervals of the previous symbol’s interval, proportional to their joint probability.

For example:
- If symbol "a" has a probability of $$\frac{1}{5}$$ and is assigned to the interval $$[0, 0.2)$$, 
- The sequence "aa" would be encoded as $$[0, 0.04)$$.

This process iterates over the entire sequence, producing nested subintervals. Any real number within the final subinterval uniquely identifies the sequence.

## Efficiency

In practice, the **final subinterval**'s length reflects the **sequence’s joint probability**, and the smallest number of bits needed to represent a number within this interval encodes the message. The code length approximates the $$-\log_2 P(\text{sequence}) $$, consistent with entropy.

Let $$x_n$$ be a message of length $n$ and $C(x_n)$ its codeword, under an assumed probability distribution $Q$. The length of the code $|C(x_n)|$ satisfies:

$$ |C(x_n)| < \lceil -\log_2 Q(x_n) \rceil + 1 $$

If the true distribution is $P$, the average code length is bounded by $H[P,Q] + 2$. Unlike Huffman coding, arithmetic coding’s overhead is spread across all symbols, achieving greater efficiency for long messages. Per symbol, the overhead is approximately $\frac{2}{n}$ bits compared to Huffman coding’s 1 bit per symbol.

### First-In-First-Out Structure

Arithmetic coding implements a **first-in-first-out (FIFO)** data structure, meaning symbols encoded first are also decoded first. This makes it especially useful in compression methods that involve autoregressive models.

### An example

To input an input message `'abac'`, first compute the probability dictionary:

```python
{'a': 0.5, 'b': 0.25, 'c': 0.25}
```

Next, create intervals for each symbol based on their probabilities:
```python
{'a': (0.0, 0.5), 'b': (0.5, 0.75), 'c': (0.75, 1.0)}
```

First 'a' is encoded into [0, 0.5] using its interval.

Then encode 'ab', using the range of old interval being 0.5 and interval of 'b' being [0.5, 0.75]:
```python
range = 0.5 - 0 = 0
low =0 + 0.5 * 0.5 = 0.25
high = 0 + 0.5 * 0.75 = 0.375
interval = [0.25, 0.375]
```

Then encode 'aba', using the range of old interval being 0.125 and interval of 'a' being [0, 0.5]:
```python
range = high - low = 0.375 - 0.25 = 0.125
low = 0.25 + 0.0 * 0.125 = 0.25
high = 0.25 + 0.5 * 0.125 = 0.3125
interval = [0.25, 0.3125]
```

Then encode 'abac', using interval of 'c' being [0.75, 1.0], and return final encoded value:
```python
range = high - low = 0.3125 - 0.25 = 0.0625
low = 0.25 + 0.75 * 0.0625 = 0.296875
high = 0.25 + 1.0 * 0.0625 = 0.3125
interval = [0.296875, 0.3125]
encoded_value = (0.296875 + 0.3125) / 2 = 0.3046875
```

To try different examples yourself, just run the `arithmetic.py` file



# Asymmetric Numeral Systems (ANS)

Another example of a streaming code is **asymmetric numeral systems (ANS)**. While arithmetic coding operates as a queue (FIFO), ANS functions as a **stack** or **last-in-first-out (LIFO)** structure, where the last symbol encoded is the first to be decoded.

## Concept

Numeral systems like decimal or binary are optimal codes for uniform distributions over a finite alphabet. They encode a sequence of symbols into a single integer, called the **stack**. 

- **Encoding:** Multiply the stack by the base (e.g., 2 or 10) and add the symbol.
- **Decoding:** Recover the symbol as the stack modulo the base, and reduce the stack by dividing it by the base.

The length of the stack, in binary, approximates the number of symbols multiplied by the logarithm of the numeral system's base, consistent with entropy coding.

### ANS Generalization

ANS extends this concept to **non-uniform probability distributions**. Symbols are mapped to subintervals of the unit interval, and this interval is discretized using a fine grid. Each point in the grid corresponds to a symbol, forming a new alphabet that can be encoded with a numeral system. Although there is redundancy in encoding, ANS avoids this through **bits-back coding**.

Like arithmetic coding, ANS incurs an overhead of up to 2 bits per message.
