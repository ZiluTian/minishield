define ptr @address_taken(){
	entry:
		br label %target
	target:
		ret ptr blockaddress(@address_taken, %target)
}
