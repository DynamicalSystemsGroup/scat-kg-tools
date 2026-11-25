# koi-07-what-koi-is-and-the-rid

Source: ant-rdf `wiki/Actant-koi--koi-infrastructure.md`; `wiki/Actant-koi--rid.md`; `briefs/koi-architectural-network.md` (Description and participating actants)

Field note, architectural view. KOI stands for Knowledge Organization Infrastructure. It is a protocol for organising knowledge where authority is scoped. It runs across subnets and coordinator nodes. The doctrine frames the assembly in terms of "ASoT" and "MOSA" (the brief uses these abbreviations without spelling them out) and sets it against two things: a single source of truth, and a walled garden. It is explicitly neither.

The infrastructure performs six functions of identification. The sources name the six as a set but do not list them in the pages the facilitator read. It works over Resource Identifiers, called RIDs.

The RID is the stable handle the infrastructure gives a resource. With it a resource can be referred to, related to other things, updated and forgotten across subnets, and no single source of truth is needed for that. That is what the RID is for: the same handle is used to refer to the resource wherever it is met.

Alongside RIDs the doctrine uses FUN signals. There are three: new, update and forget. These are how a change to a resource is sent through the infrastructure. They connect what people want to do with a resource (add it, change it, withdraw it) to the protocol. The forget signal is the one that figures in the forget incident.

The doctrine also names per-relationship discipline. The sources give no more detail on it in the pages read.
