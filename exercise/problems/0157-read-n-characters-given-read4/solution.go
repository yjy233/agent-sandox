package main

type Solution struct {
	*Read4Source
}

func (s *Solution) read(buf []byte, n int) int {
	// 调用 s.Read4(buf4) 每次最多读 4 字节
	panic("TODO")
}
