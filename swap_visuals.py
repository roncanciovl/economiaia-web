import re

file_path = 'd:/workspace/marketing_ws/resources/teoria_senal_creativa.html'
with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Instead of one huge regex, let's chunk it properly.
# We are looking for exactly the 5 blocks.

def swap_blocks(html):
    # Pattern designed to capture:
    # 1: Container start
    # 2: Text div start (up to padding: 2.5rem;)
    # 3: border-right styling
    # 4: rest of text div + closing div (position: relative; ... </div>)
    # 5: Visual div start (<!-- Visual ... --> <div ...) up to closing div
    
    pattern = re.compile(
        r'(<div\s+style=[\"\']display:\s*flex;\s*flex-wrap:\s*wrap;.*?[\"\']>)\s*(<div\s+style=[\"\']flex:\s*1;\s*min-width:\s*300px;\s*padding:\s*2\.5rem;\s*)(border-right:\s*1px\s+solid\s+#[0-9a-fA-F]+;\s*)(position:\s*relative;[\"\']>.*?</div>)\s*(<!--\s*Visual.*?-->\s*<div\s+style=[\"\']flex:\s*1;\s*min-width:\s*300px;\s*.*?display:\s*flex;.*?overflow:\s*hidden;)([\"\']>.*?</div>)', 
        re.DOTALL
    )
    
    def repl(match):
        wrapper_start = match.group(1)
        text_start_1 = match.group(2)
        border_right = match.group(3)
        text_content = match.group(4)
        
        visual_start = match.group(5)
        visual_content = match.group(6)
        
        # Text block without border_right:
        new_text_block = text_start_1 + text_content
        
        # Visual block WITH border_right in its style:
        new_visual_block = visual_start + " border-bottom: 1px solid #334155; " + border_right.strip() + ";" + visual_content
        
        # Reorder
        return f"{wrapper_start}\n                {new_visual_block}\n                {new_text_block}"

    new_html, num_subs = pattern.subn(repl, html)
    print(f"Replaced {num_subs} blocks.")
    return new_html

new_html = swap_blocks(html)
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_html)
