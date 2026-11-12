define i32 @select_case(i32 %value) {
entry:
  switch i32 %value, label %other [
    i32 0, label %zero
    i32 1, label %one
  ]
zero:
  ret i32 10
one:
  ret i32 20
other:
  ret i32 -1
}
