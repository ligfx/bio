SOURCES := $(wildcard *.ffa)
ROOTS := $(patsubst %.ffa, %, $(SOURCES))
PHR := $(patsubst %, %.phr, $(ROOTS))
PIN := $(patsubst %, %.pin, $(ROOTS))
PSQ := $(patsubst %, %.psq, $(ROOTS))
OUT := $(PHR) $(PIN) $(PSQ)

all: $(OUT)

%.phr %.pin %.psq: %.ffa
	formatdb -t $(patsubst %.ffa, %, $<) -i $< -n $(patsubst %.ffa, %, $<) -p T
