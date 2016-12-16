from tendrl.common.atoms.base_atom import BaseAtom


class VolumeNotExists(BaseAtom):
    def run(self, parameters):
        return True
