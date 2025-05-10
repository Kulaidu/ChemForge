#import pubchempy as pcp
from rdkit import Chem
from rdkit.Chem import AllChem, Draw, inchi
import itertools
import io
import base64
import chemcursor

def validate_elements(elements):
    print("Validating Elements")
    VALID_ELEMENTS = {
        "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", 
        "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", 
        "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", 
        "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", 
        "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr"
    }
    for elem in elements:
        if elem not in VALID_ELEMENTS:
            return False, elem
    return True, None

def chemi_root(formula):
    elements = {}
    i = 0
    while i < len(formula):
        if formula[i].isupper():
            elem = formula[i]
            i += 1
            while i < len(formula) and formula[i].islower():
                elem += formula[i]
                i += 1
            count = ""
            while i < len(formula) and formula[i].isdigit():
                count += formula[i]
                i += 1
            if count == "":
                count = 1
            elements[elem] = int(count)
        else:
            i += 1

    return elements

'''
TO DELETE
def search_pubchem(permuted_formula):
    if pubchem_available:
        try:
            compounds = pcp.get_compounds(permuted_formula, 'formula')
            if compounds:
                return [{
                    'Molecular Formula': compound.molecular_formula,
                    'Molecular Weight': compound.molecular_weight,
                    'IUPAC Name': compound.iupac_name if compound.iupac_name else (str(compound.synonyms[0]) if compound.synonyms else "N/A"),
                    'SMILES': compound.canonical_smiles,
                    'InChI': compound.inchi,
                    'InChIKey': compound.inchikey 
                    } for compound in compounds]
        except Exception as e:
            print(f"PubChem search failed: {e}")
    return []
'''

def generate_3d_structure(inchi_str):
    print(f"Generating 3D for {inchi_str}")
    if not inchi_str:
        return None

    if not inchi_str.startswith("InChI="):
        inchi_str = "InChI=" + inchi_str

    try:
        mol = inchi.MolFromInchi(inchi_str)
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol)
        AllChem.MMFFOptimizeMolecule(mol)
        return mol
    except Exception as e:
        print(f"Error generating 3D structure: {str(e)}")
        return None

def generate_2d_structure(inchi_str):
    print(f"Generating 2D for {inchi_str}")
    if not inchi_str:
        return None

    if not inchi_str.startswith("InChI="):
        inchi_str = "InChI=" + inchi_str

    try:
        mol = inchi.MolFromInchi(inchi_str)
        mol = Chem.AddHs(mol)
        options = Draw.MolDrawOptions()
        options.setBackgroundColour((0, 0, 0, 0))
        img_ld = Draw.MolToImage(mol, kekulize=False, size=(300,300), options=options)
        img_byte_arr = io.BytesIO()
        img_ld.save(img_byte_arr, format='PNG')
        img_ld_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
        return img_ld_base64
    except Exception as e:
        print(f"Error generating 2D structure: {str(e)}")
        return None

def formulasubscript(formula):
    subscripts = {
        "0": "₀", "1": "₁","2": "₂", "3": "₃", "4": "₄",
        "5": "₅", "6": "₆", "7": "₇", "8": "₈", "9": "₉"
    }
    subscripted = ''.join(subscripts[char] if char in subscripts else char for char in formula)
    return subscripted

def get_components(formula):
    ELEMENT_NAMES = {
        "H": "Hydrogen", "He": "Helium", "Li": "Lithium", "Be": "Beryllium", "B": "Boron",
        "C": "Carbon", "N": "Nitrogen", "O": "Oxygen", "F": "Fluorine", "Ne": "Neon",
        "Na": "Sodium", "Mg": "Magnesium", "Al": "Aluminum", "Si": "Silicon", "P": "Phosphorus",
        "S": "Sulfur", "Cl": "Chlorine", "Ar": "Argon", "K": "Potassium", "Ca": "Calcium",
        "Sc": "Scandium", "Ti": "Titanium", "V": "Vanadium", "Cr": "Chromium", "Mn": "Manganese",
        "Fe": "Iron", "Co": "Cobalt", "Ni": "Nickel", "Cu": "Copper", "Zn": "Zinc",
        "Ga": "Gallium", "Ge": "Germanium", "As": "Arsenic", "Se": "Selenium", "Br": "Bromine",
        "Kr": "Krypton", "Rb": "Rubidium", "Sr": "Strontium", "Y": "Yttrium", "Zr": "Zirconium",
        "Nb": "Niobium", "Mo": "Molybdenum", "Tc": "Technetium", "Ru": "Ruthenium", "Rh": "Rhodium",
        "Pd": "Palladium", "Ag": "Silver", "Cd": "Cadmium", "In": "Indium", "Sn": "Tin",
        "Sb": "Antimony", "Te": "Tellurium", "I": "Iodine", "Xe": "Xenon", "Cs": "Cesium",
        "Ba": "Barium", "La": "Lanthanum", "Ce": "Cerium", "Pr": "Praseodymium", "Nd": "Neodymium",
        "Pm": "Promethium", "Sm": "Samarium", "Eu": "Europium", "Gd": "Gadolinium", "Tb": "Terbium",
        "Dy": "Dysprosium", "Ho": "Holmium", "Er": "Erbium", "Tm": "Thulium", "Yb": "Ytterbium",
        "Lu": "Lutetium", "Hf": "Hafnium", "Ta": "Tantalum", "W": "Tungsten", "Re": "Rhenium",
        "Os": "Osmium", "Ir": "Iridium", "Pt": "Platinum", "Au": "Gold", "Hg": "Mercury",
        "Tl": "Thallium", "Pb": "Lead", "Bi": "Bismuth", "Po": "Polonium", "At": "Astatine",
        "Rn": "Radon", "Fr": "Francium", "Ra": "Radium", "Ac": "Actinium", "Th": "Thorium",
        "Pa": "Protactinium", "U": "Uranium", "Np": "Neptunium", "Pu": "Plutonium", "Am": "Americium",
        "Cm": "Curium", "Bk": "Berkelium", "Cf": "Californium", "Es": "Einsteinium", "Fm": "Fermium",
        "Md": "Mendelevium", "No": "Nobelium", "Lr": "Lawrencium"
    }
    
    composed_of = chemi_root(formula)

    components = []
    for element, count in composed_of.items():
        element_name = ELEMENT_NAMES[element]
        components.append(f"{count} {element_name}")
    
    return ", ".join(components)

def generate_structure(id):
    print("Generating structure of id: " + id)
    id_query = chemcursor.retrieve_compound(id)

    try:
        id, name, formula, inchi_str, weight, color, form, bond_type = id_query
                
        img_ld_base64 = generate_2d_structure(inchi_str)
        mol_3d = generate_3d_structure(inchi_str)
        mb = Chem.MolToMolBlock(mol_3d)

        components = get_components(formula)
        formula = formulasubscript(formula)

        return {
            'name': name,
            'formula': formula,
            'InChI': inchi_str,
            'mol_weight': weight,
            'color': color,
            'form': form,
            'bond_type': bond_type,
            'components': components,
            'image2d': img_ld_base64,
            'mol_block': mb
        }

    except Exception as e:
        print(f"Error processing molecule: {str(e)}")
        return {'error': f"Failed to process molecule: {str(e)}"}

def retrieve_compounds(formula):
    elements = chemi_root(formula)

    is_valid, invalid_element = validate_elements(elements)
    if not is_valid:
        return {'error': f'Invalid element: {invalid_element}'}

    combined_elements = []
    for elem, count in elements.items():
        if count == 1:
            combined_elements.append(elem)
        else:
            combined_elements.append(f"{elem}{count}")
    print("Combined elements:", combined_elements)

    unique_permutations = set(itertools.permutations(combined_elements))
    possible_formulas = ["".join(perm) for perm in unique_permutations]

    results = chemcursor.search_database(possible_formulas, combined_elements)
    if not results:
        return {'error': 'Compound not found in database'}

    compounds = []
    for result in results:
        if len(result) != 4:
            print(f"Skipping malformed result: {result}")
            continue
        print(result)
        id, name, formula, inchi_str = result
        formula = formulasubscript(formula)
        struc_2d = generate_2d_structure(inchi_str)
        compounds.append({
        'id': id,
        'name': name,
        'formula': formula,
        'structure_image': struc_2d
    })

    return compounds