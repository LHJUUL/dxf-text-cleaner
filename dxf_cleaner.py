#!/usr/bin/env python3
"""
DXF CLEANER - Comprehensive Text and Annotation Removal Tool
Created from lessons learned cleaning Norwegian architectural DXF files

Removes:
- TEXT and MTEXT entities (loose text)
- ATTDEF in block definitions (attribute templates)
- ATTRIB attached to INSERT entities (attribute values like "1/2")
- DIMENSION entities (mållinjer)
- Text in anonymous (*U, *D) blocks
- Specified layers
- Xref references

Usage:
    python dxf_cleaner.py input.dxf [options]
    
    Or interactive mode:
    python dxf_cleaner.py
"""

import ezdxf
import argparse
import sys
from pathlib import Path
from typing import Set, Dict


class DXFCleaner:
    """Comprehensive DXF cleaning utility"""
    
    def __init__(self):
        self.stats = {
            'modelspace_removed': 0,
            'block_text_removed': 0,
            'attrib_removed': 0,
            'blocks_processed': 0,
            'anonymous_blocks_processed': 0,
            'inserts_processed': 0
        }
        
    def clean_file(
        self,
        input_file: Path,
        output_file: Path,
        remove_text: bool = True,
        remove_dimensions: bool = True,
        remove_attribs: bool = True,
        remove_layers: Set[str] = None,
        remove_text_from_blocks: bool = True,
        include_anonymous_blocks: bool = True,
        remove_xrefs: bool = True
    ) -> Dict:
        """
        Clean DXF file with specified options
        
        Args:
            input_file: Path to input DXF
            output_file: Path to output DXF
            remove_text: Remove TEXT/MTEXT entities
            remove_dimensions: Remove DIMENSION entities
            remove_attribs: Remove ATTDEF and attached ATTRIB
            remove_layers: Set of layer names to remove
            remove_text_from_blocks: Remove text from block definitions
            include_anonymous_blocks: Also clean *U and *D blocks
            remove_xrefs: Remove Xref layers
        
        Returns:
            Dictionary with statistics
        """
        print(f"\n{'='*70}")
        print(f"DXF CLEANER")
        print(f"{'='*70}\n")
        
        # Load file
        print(f"📂 Loading: {input_file.name}")
        doc = ezdxf.readfile(input_file)
        msp = doc.modelspace()
        
        # Build entity types to remove
        entity_types_to_skip = set()
        
        if remove_text:
            entity_types_to_skip.update(['TEXT', 'MTEXT'])
        
        if remove_dimensions:
            entity_types_to_skip.update([
                'DIMENSION', 'ALIGNED_DIMENSION', 'ROTATED_DIMENSION',
                'LINEAR_DIMENSION', 'DIAMETRIC_DIMENSION', 
                'RADIAL_DIMENSION', 'ANGULAR_DIMENSION'
            ])
        
        if remove_attribs:
            entity_types_to_skip.update(['ATTRIB', 'ATTDEF'])
        
        # Build layers to skip
        layers_to_skip = remove_layers or set()
        if remove_xrefs:
            # Common Xref layer patterns
            for layer in self._get_all_layers(doc):
                if any(pattern in layer for pattern in ['Xref', 'xref', 'XREF']):
                    layers_to_skip.add(layer)
        
        # STEP 1: Clean modelspace
        print(f"\n🔍 STEP 1: Cleaning modelspace...")
        to_delete = []
        
        for entity in msp:
            entity_type = entity.dxftype()
            layer = entity.dxf.layer
            
            if entity_type in entity_types_to_skip:
                to_delete.append(entity)
                continue
            
            if layer in layers_to_skip:
                to_delete.append(entity)
                continue
        
        for entity in to_delete:
            msp.delete_entity(entity)
        
        self.stats['modelspace_removed'] = len(to_delete)
        print(f"   ✓ Removed {len(to_delete)} entities")
        
        # STEP 2: Clean block definitions
        if remove_text_from_blocks:
            print(f"\n🔍 STEP 2: Cleaning block definitions...")
            
            for block in doc.blocks:
                block_name = block.name
                
                # Skip layout blocks
                if block_name in ['*Model_Space', '*Paper_Space', '*Paper_Space0']:
                    continue
                
                # Skip anonymous blocks if requested
                if not include_anonymous_blocks and block_name.startswith('*'):
                    continue
                
                self.stats['blocks_processed'] += 1
                
                if block_name.startswith('*'):
                    self.stats['anonymous_blocks_processed'] += 1
                
                to_delete_from_block = []
                
                for entity in block:
                    if entity.dxftype() in entity_types_to_skip:
                        to_delete_from_block.append(entity)
                
                for entity in to_delete_from_block:
                    block.delete_entity(entity)
                    self.stats['block_text_removed'] += 1
            
            print(f"   ✓ Processed {self.stats['blocks_processed']} blocks")
            print(f"   ✓ Including {self.stats['anonymous_blocks_processed']} anonymous (*U/*D) blocks")
            print(f"   ✓ Removed {self.stats['block_text_removed']} text entities")
        
        # STEP 3: Remove attached ATTRIB from INSERT entities
        if remove_attribs:
            print(f"\n🔍 STEP 3: Removing attached ATTRIB from INSERT entities...")
            
            for entity in msp:
                if entity.dxftype() == 'INSERT':
                    if hasattr(entity, 'attribs') and len(entity.attribs) > 0:
                        self.stats['inserts_processed'] += 1
                        attrib_count = len(entity.attribs)
                        entity.attribs.clear()
                        self.stats['attrib_removed'] += attrib_count
            
            print(f"   ✓ Processed {self.stats['inserts_processed']} INSERT entities")
            print(f"   ✓ Removed {self.stats['attrib_removed']} attached ATTRIB")
        
        # Save
        print(f"\n💾 Saving cleaned file...")
        doc.saveas(output_file)
        
        # Report
        total_removed = (
            self.stats['modelspace_removed'] + 
            self.stats['block_text_removed'] + 
            self.stats['attrib_removed']
        )
        
        print(f"\n{'='*70}")
        print(f"✅ CLEANING COMPLETE!")
        print(f"{'='*70}")
        print(f"\n📊 STATISTICS:")
        print(f"  Modelspace entities removed: {self.stats['modelspace_removed']}")
        print(f"  Block text removed: {self.stats['block_text_removed']}")
        print(f"  Attached ATTRIB removed: {self.stats['attrib_removed']}")
        print(f"  TOTAL REMOVED: {total_removed}")
        print(f"\n✓ Output: {output_file.name}")
        print(f"{'='*70}\n")
        
        return self.stats
    
    def _get_all_layers(self, doc):
        """Get all layer names from document"""
        layers = set()
        for layer in doc.layers:
            layers.add(layer.dxf.name)
        return layers
    
    def analyze_file(self, filepath: Path):
        """Analyze DXF and show what would be removed"""
        doc = ezdxf.readfile(filepath)
        msp = doc.modelspace()
        
        print(f"\n{'='*70}")
        print(f"DXF FILE ANALYSIS: {filepath.name}")
        print(f"{'='*70}\n")
        
        # Count entities by type
        entity_types = {}
        for entity in msp:
            t = entity.dxftype()
            entity_types[t] = entity_types.get(t, 0) + 1
        
        print("ENTITY TYPES IN MODELSPACE:")
        for t, count in sorted(entity_types.items()):
            marker = "✗" if t in ['TEXT', 'MTEXT', 'DIMENSION', 'ATTRIB'] else "✓"
            print(f"  {marker} {t}: {count}")
        
        # Count entities in blocks
        block_text_count = 0
        anonymous_block_count = 0
        for block in doc.blocks:
            if block.name.startswith('*'):
                if block.name not in ['*Model_Space', '*Paper_Space', '*Paper_Space0']:
                    anonymous_block_count += 1
            
            for entity in block:
                if entity.dxftype() in ['TEXT', 'MTEXT', 'ATTDEF']:
                    block_text_count += 1
        
        print(f"\nBLOCKS:")
        print(f"  Total blocks: {len(doc.blocks) - 3}")  # Exclude layout blocks
        print(f"  Anonymous (*U/*D) blocks: {anonymous_block_count}")
        print(f"  ✗ Text entities in blocks: {block_text_count}")
        
        # Count INSERT with attached ATTRIB
        inserts_with_attribs = 0
        attrib_count = 0
        for entity in msp:
            if entity.dxftype() == 'INSERT':
                if hasattr(entity, 'attribs') and len(entity.attribs) > 0:
                    inserts_with_attribs += 1
                    attrib_count += len(entity.attribs)
        
        print(f"\nINSERT ENTITIES WITH ATTACHED ATTRIB:")
        print(f"  ✗ INSERT blocks with attributes: {inserts_with_attribs}")
        print(f"  ✗ Total attached ATTRIB: {attrib_count}")
        
        # Show layers
        layers = self._get_all_layers(doc)
        xref_layers = [l for l in layers if any(x in l for x in ['Xref', 'xref', 'XREF'])]
        
        print(f"\nLAYERS:")
        print(f"  Total layers: {len(layers)}")
        if xref_layers:
            print(f"  ✗ Xref layers: {len(xref_layers)}")
            for layer in xref_layers[:5]:
                print(f"    - {layer}")
        
        print(f"\n{'='*70}\n")


def main():
    parser = argparse.ArgumentParser(
        description='DXF Cleaner - Remove text and annotations from DXF files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Clean with default settings (remove everything)
  python dxf_cleaner.py input.dxf
  
  # Analyze without cleaning
  python dxf_cleaner.py input.dxf --analyze
  
  # Keep dimensions but remove text
  python dxf_cleaner.py input.dxf --keep-dimensions
  
  # Remove specific layers
  python dxf_cleaner.py input.dxf --remove-layers "Skissestreker,a270--t"
  
  # Interactive mode
  python dxf_cleaner.py
        """
    )
    
    parser.add_argument('input', nargs='?', help='Input DXF file')
    parser.add_argument('-o', '--output', help='Output DXF file (default: input_CLEAN.dxf)')
    parser.add_argument('--analyze', action='store_true', help='Analyze file without cleaning')
    parser.add_argument('--add-date', action='store_true', help='Add date to output filename (input_CLEAN_20250414.dxf)')
    parser.add_argument('--keep-text', action='store_true', help='Keep TEXT/MTEXT entities')
    parser.add_argument('--keep-dimensions', action='store_true', help='Keep DIMENSION entities')
    parser.add_argument('--keep-attribs', action='store_true', help='Keep ATTRIB entities')
    parser.add_argument('--skip-blocks', action='store_true', help='Skip cleaning block definitions')
    parser.add_argument('--skip-anonymous', action='store_true', help='Skip anonymous (*U/*D) blocks')
    parser.add_argument('--keep-xrefs', action='store_true', help='Keep Xref layers')
    parser.add_argument('--remove-layers', help='Comma-separated list of layers to remove')
    
    args = parser.parse_args()
    
    cleaner = DXFCleaner()
    
    # Interactive mode if no input
    if not args.input:
        print("\n" + "="*70)
        print("DXF CLEANER - Interactive Mode")
        print("="*70 + "\n")
        
        input_file = input("Enter input DXF file path: ").strip().strip('"')
        input_path = Path(input_file)
        
        if not input_path.exists():
            print(f"❌ Error: File not found: {input_path}")
            return 1
        
        # Show analysis
        cleaner.analyze_file(input_path)
        
        # Ask what to do
        action = input("Action: (c)lean, (q)uit: ").lower()
        
        if action != 'c':
            print("Cancelled.")
            return 0
        
        # Get output path
        default_output = input_path.parent / f"{input_path.stem}_CLEAN.dxf"
        output = input(f"Output file [{default_output.name}]: ").strip() or str(default_output)
        output_path = Path(output)
        
        # Clean with default settings
        cleaner.clean_file(
            input_path,
            output_path,
            remove_text=True,
            remove_dimensions=True,
            remove_attribs=True,
            remove_text_from_blocks=True,
            include_anonymous_blocks=True,
            remove_xrefs=True
        )
        
        return 0
    
    # Command line mode
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"❌ Error: File not found: {input_path}")
        return 1
    
    # Analysis mode
    if args.analyze:
        cleaner.analyze_file(input_path)
        return 0
    
    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        # Add date suffix if requested
        if args.add_date:
            from datetime import datetime
            date_str = datetime.now().strftime("%Y%m%d")
            output_path = input_path.parent / f"{input_path.stem}_CLEAN_{date_str}.dxf"
        else:
            output_path = input_path.parent / f"{input_path.stem}_CLEAN.dxf"
    
    # Parse layers to remove
    remove_layers = set()
    if args.remove_layers:
        remove_layers = {l.strip() for l in args.remove_layers.split(',')}
    
    # Clean
    cleaner.clean_file(
        input_path,
        output_path,
        remove_text=not args.keep_text,
        remove_dimensions=not args.keep_dimensions,
        remove_attribs=not args.keep_attribs,
        remove_layers=remove_layers,
        remove_text_from_blocks=not args.skip_blocks,
        include_anonymous_blocks=not args.skip_anonymous,
        remove_xrefs=not args.keep_xrefs
    )
    
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
