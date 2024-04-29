# Student card processing
## 1.Read the image
![alt text](<ProcessedImages/z5393034160252_8edb2fa38b6bea0b262bb837aa68da53.jpg>)
## 2.Smoothing the card by erosion and dilation algorithm
![alt text](<ProcessedImages/z5393035503928_53d4184a8ef9c2ef900fb6999398acaa.jpg>)
## 3.Get the boundaries of the card by using Houghline
![alt text](<ProcessedImages/z5393036149344_0f659dbe4990f8bdba5d7d5c0c7751e1.jpg>)
## 4. Get 4 intersecting points of 4 lines. The points is presented as blue points
![alt text](<ProcessedImages/z5393036784636_50bb84ac06f4aacffd9c62f0e1caf7ba.jpg>)
## 5. Using affine transform to crop the student card from image
![alt text](<ProcessedImages/z5393037158412_1427bc3387cdcb7427277ceb9b4c66b6.jpg>)
## 6. Specify the coordinate of each information field in the cropped image
![alt text](<ProcessedImages/z5393082283274_b10f0cab5e727e3c58ff9dc4dfdce6e7.jpg>) ![alt text](<ProcessedImages/z5393082766725_1cf2eeedf3874ab2155a84e3f2d03c4d.jpg>) ![alt text](<ProcessedImages/z5393083206754_03e630616005dcad4b1bfdadbe319505.jpg>) ![alt text](<ProcessedImages/z5393083649764_dd130eb7b5ee601d5bd1f9bd0d2cd446.jpg>) ![alt text](<ProcessedImages/z5393084032414_b759c0e736157602b1aaf88a4ee3af19.jpg>) ![alt text](<ProcessedImages/z5393084432962_b4c4cfaa2c012d955d50af9993fc19ca.jpg>) ![alt text](<ProcessedImages/z5393085209453_c155f2eb5bba93a11184e4fdc7a77092.jpg>)
## 7. Use vietocr model to read the informations
![alt text](<ProcessedImages/z5393037580020_95508a4a697439d2265d280d88d4b618.jpg>)
