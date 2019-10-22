Câu 1:
  1. Hàm evaluationFunction trả về giá trị value, với:
  2. Đầu tiên ta gán value = điểm hiện tại
  3. value = value -10.0/(khoảng cách manhattan từ pacman đến ghost) + 
      10.0/(khoảng cách manhattan từ pacman đến thức ăn gần nhất)
  
Câu 2:
  1. Đầu tiên nếu là trạng thái kết thúc của game thì trả về điểm
  2. Nếu là trạng thái kết thúc của Ghost thì giảm độ sâu đi 1, ngược lại trả về độ sâu hiện tại
  3. Danh sách các action
  4. Nếu là ghost thì trả về min, nếu là pacman thì trả về max
 
Câu 3: 
  1. Hàm getMaxValue trả về giá trị max tốt nhất và hành động tương ứng
  2. Hàm getMinValue trả về giá trị min tốt nhất và hành động tương ứng
  
Câu 4: 
  Làm tương tự như với câu 2, nhưng thay vì trả về min cho Ghost ta trả về average
