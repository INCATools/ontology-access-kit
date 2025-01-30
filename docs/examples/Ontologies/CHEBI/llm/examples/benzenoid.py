from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors


def is_benzenoid(smiles: str):
    """
    Determines if a molecule is a benzenoid (benzene or substituted benzene).

    Args:
        smiles (str): SMILES string of the molecule

    Returns:
        bool: True if molecule is a benzenoid, False otherwise
        str: Reason for classification
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False, "Invalid SMILES string"

    # Generate the aromatic ring information
    rings = mol.GetRingInfo()

    # Check for at least one 6-membered ring
    if not any(len(ring) == 6 for ring in rings.AtomRings()):
        return False, "No 6-membered rings found"

    # Find all aromatic 6-membered rings
    aromatic_rings = []
    for ring in rings.AtomRings():
        if len(ring) == 6:
            atoms = [mol.GetAtomWithIdx(i) for i in ring]
            if all(atom.GetIsAromatic() for atom in atoms):
                aromatic_rings.append(ring)

    if not aromatic_rings:
        return False, "No aromatic 6-membered rings found"

    # Check if all carbons in the aromatic ring are carbon
    for ring in aromatic_rings:
        atoms = [mol.GetAtomWithIdx(i) for i in ring]
        if not all(atom.GetSymbol() == 'C' for atom in atoms):
            return False, "Ring contains non-carbon atoms"

    # Check substituents
    ring_atoms = set(aromatic_rings[0])
    substituents = []

    for atom_idx in ring_atoms:
        atom = mol.GetAtomWithIdx(atom_idx)
        for neighbor in atom.GetNeighbors():
            if neighbor.GetIdx() not in ring_atoms:
                substituents.append(neighbor.GetSymbol())

    if len(substituents) > 0:
        return True, f"Substituted benzene with substituents: {', '.join(set(substituents))}"
    else:
        return True, "Unsubstituted benzene"
