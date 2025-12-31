# High level concept

1. Universal Coded Character Set (UCS): Each UCS character is abstractly represented by a code point, an integer between 0 and 1,114,111 ($1114112 = 2^{20} + 2^{16}$ or $17 × 2^{16} =$ 0x110000  code points), used to represent each character within the internal logic of text processing software.

2. As of [Unicode 17.0](https://www.unicode.org/Public/17.0.0/ucd/Scripts.txt), released in September 2025, of the 1.11 million code-points:
   - 810,304 (73%) are unallocated
   - 303,808 (27%) are allocated
     - [159,866 (14%) have been assigned characters](/files/df_unicode17_scripts.tsv)
       - 159,629 graphical characters (some of which do not have a visible glyph, but are still counted as graphical)
       - 237 special purpose characters for control and formatting.
     - 137,468 (12%) are reserved for private use
     - 2,048 are used to enable the mechanism of surrogates
     - 66 are designated as noncharacters
# Key URLs
1. [UCS Wiki](https://en.wikipedia.org/wiki/Universal_Character_Set_characters)
2. [Unicode 17 Scripts](https://www.unicode.org/Public/17.0.0/ucd/Scripts.txt)
3. [ISO 15924](https://unicode.org/iso15924/iso15924-codes.html)
   -  This yields 227 [language-script-names](/files/df_iso15924_scripts.tsv)
