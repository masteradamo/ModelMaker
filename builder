tarfil = raw_input("TARGET FILE PATH: ")
cwin = raw_input("CONTEXT WINDOW SIZA: ")

import stripper #reads - corpus; writes - linus
stripper.runner(tarfil)
import numcounter #reads - linus; writes - numbus
import replacer #reads - linus, numbus; writes - numlus
import numfrequer #reads - numlus; writes - frequs, contextus
numfrequer.runner(cwin)
import numtaler #reads - frequs, contextus; writes - tallus
import numturner #reads - tallus, contextus; writes - CONTEXTS
