define i32 @merge(i1 %condition) {
entry:
  br i1 %condition, label %left, label %right
left:
  br label %join
right:
  br label %join
join:
  %value = phi i32 [ 10, %left ], [ 20, %right ]
  ret i32 %value
}
