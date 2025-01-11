
import xml.etree.ElementTree as ET
import sys
from uuid import uuid4

def interpolate_presets(xml1: str, xml2: str, amount: float) -> str:
    """Simple preset interpolator that works directly with XML strings."""
    
    # Parse the XMLs
    root1 = ET.fromstring(xml1)
    root2 = ET.fromstring(xml2)
    
    # Create new preset from the first one (as template)
    new_root = ET.fromstring(xml1)
    
    # Update UUID
    meta = new_root.find('.//Meta')
    if meta is not None:
        meta.set('UUID', str(uuid4()))
    
    # Get all parameters with values
    params1 = root1.findall('.//Parameters/*')
    params2 = root2.findall('.//Parameters/*')
    new_params = new_root.findall('.//Parameters/*')
    
    # Interpolate each parameter
    for p1, p2, new_p in zip(params1, params2, new_params):
        try:
            # Get unmapped values
            u1 = float(p1.get('unmapped_value', '0'))
            u2 = float(p2.get('unmapped_value', '0'))
            
            # Get mapped values
            m1 = float(p1.get('mapped_value', '0'))
            m2 = float(p2.get('mapped_value', '0'))
            
            # Calculate interpolated values
            new_unmapped = u1 + (u2 - u1) * amount
            new_mapped = m1 + (m2 - m1) * amount
            
            # Set new values
            new_p.set('unmapped_value', f"{new_unmapped}")
            new_p.set('mapped_value', f"{new_mapped}")
        except Exception as e:
            print(f"Warning: Couldn't interpolate parameter {p1.tag}: {e}")
            continue
    
    # Convert back to string
    return ET.tostring(new_root, encoding='unicode', xml_declaration=True)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 interpolate.py preset1.xml preset2.xml amount")
        print("Example: python3 interpolate.py lead1.xml lead2.xml 0.5")
        sys.exit(1)
        
    # Read input files
    with open(sys.argv[1], 'r') as f:
        xml1 = f.read()
    with open(sys.argv[2], 'r') as f:
        xml2 = f.read()
        
    # Get interpolation amount
    amount = float(sys.argv[3])
    
    # Generate new preset
    new_preset = interpolate_presets(xml1, xml2, amount)
    
    # Generate output filename
    outfile = f"interpolated_{amount}.xml"
    
    # Save the result
    with open(outfile, 'w') as f:
        f.write(new_preset)
        
    print(f"Created new preset: {outfile}")
