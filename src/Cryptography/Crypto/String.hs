module Cryptography.Crypto.String where

import Data.Char
import Data.Word
import Data.Bits
import qualified Data.ByteString as B
import qualified Data.ByteString.Char8 as BC
import qualified Data.ByteString.Lazy.Char8 as LBC
import Data.ByteString.Builder

fromAscii :: String -> B.ByteString
fromAscii = BC.pack

toAscii :: B.ByteString -> String
toAscii = BC.unpack

fromHex :: String -> B.ByteString
fromHex = B.pack . map hexToWord8 . pairs . map digitToInt where hexToWord8 :: (Int, Int) -> Word8
                                                                 hexToWord8 (x, y) = fromIntegral (x * 16 + y)

toHex :: B.ByteString -> String
toHex = LBC.unpack . toLazyByteString . byteStringHex

bXor :: B.ByteString -> B.ByteString -> B.ByteString
bXor a b = B.pack $ zipWith xor (B.unpack a) (B.unpack b)

pairs :: [a] -> [(a, a)]
pairs [] = []
pairs (x:y:xs) = (x, y) : pairs xs
