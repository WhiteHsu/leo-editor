# -*- coding: utf-8 -*-
#@+leo-ver=5-thin
#@+node:ekr.20131109170017.16504: * @file leoVim.py
#@@first

'''Leo's vim emulator.'''

#@@language python
#@@tabwidth -4
#@@pagewidth 70

import leo.core.leoGlobals as g
import string

#@+others
#@+node:ekr.20140803220119.18093: ** ':' commands
#@+node:ekr.20140811180848.18153: *3* :! (shell command)
@g.command(':!')
def vim_e_exclam(event):
    '''Execute a shell command.'''
    c = event.get('c')
    if c and c.vimCommands:
        c.vimCommands.shell_command()
#@+node:ekr.20140811180848.18151: *3* :%s (substitutions)
@g.command(':%s')
def vim_substitution(event):
    '''cycle-focus'''
    c = event.get('c')
    if c and c.vimCommands:
        c.vimCommands.substitution(':%s')
#@+node:ekr.20140804202802.18152: *3* :e!
@g.command(':e!')
def vim_colon_e_exclam(event):
    '''Revert all changes to a .leo file, prompting if there have been changes.'''
    c = event.get('c')
    if c:
        c.revert()
#@+node:ekr.20140811170859.18253: *3* :gt & Gt
@g.command(':gt')
def vim_gt(event):
    '''cycle-focus'''
    c = event.get('c')
    if c and c.vimCommands:
        c.vimCommands.cycle_focus()

@g.command(':gT')
def vim_gT(event):
    '''cycle-all-focus'''
    c = event.get('c')
    if c and c.vimCommands:
        c.vimCommands.cycle_all_focus()
#@+node:ekr.20140810181832.18222: *3* :print-dot
@g.command(':print-dot')
def vim_show_dot(event):
    '''Show the vim dot.'''
    c = event.get('c')
    if c and c.vimCommands:
        c.vimCommands.print_dot()
#@+node:ekr.20140804202802.18156: *3* :q & :qa
@g.command(':q')
def vim_colon_q(event):
    '''Quit, prompting for saves.'''
    g.app.onQuit(event)
    
@g.command(':qa')
def vim_colon_qa(event):
    '''Quit only if there are no unsaved changes.'''
    for c in g.app.commanders():
        if c.isChanged():
            return
    g.app.onQuit(event)
#@+node:ekr.20140804202802.18150: *3* :r
@g.command(':r') # :r filename
def vim_colon_r(event):
    '''Put the contents of a file at the insertion point.'''
    c = event.get('c')
    if c and c.vimCommands:
        c.vimCommands.load_file_at_cursor()
#@+node:ekr.20140811211944.18163: *3* :tabnew
@g.command(':tabnew') # :tab
def vim_colon_tabnew(event):
    '''
    Prompts for a file name.
    If the file exits, opens it in a new tab.
    Otherwise, opens a tab for a new file.
    '''
    c = event.get('c')
    if c and c.vimCommands:
        c.vimCommands.tabnew()
#@+node:ekr.20140808141921.18059: *3* :toggle-vim-mode
@g.command(':toggle-vim-mode')
def toggle_vim_mode(event):
    '''Save the .leo file.'''
    c = event.get('c')
    if c and c.vimCommands:
        c.vimCommands.toggle_vim_mode()
#@+node:ekr.20140808074553.17923: *3* :toggle-vim-trainer-mode
@g.command(':toggle-vim-trainer-mode')
def toggle_vim_trainer_mode(event):
    '''Save the .leo file.'''
    c = event.get('c')
    if c and c.vimCommands:
        c.vimCommands.toggle_vim_trainer()
#@+node:ekr.20140804202802.18154: *3* :w & :wa & :wq
@g.command(':w')
def vim_colon_w(event):
    '''Save the .leo file.'''
    c = event.get('c')
    if c:
        c.save()
        
@g.command(':wa') # same as :xa
def vim_colon_wall(event):
    '''Save all open files and keep working.'''
    for c in g.app.commanders():
        if c.isChanged():
            c.save()

@g.command(':wq')
def vim_colon_wq(event):
    '''Save all open files and exit.'''
    for c in g.app.commanders():
        c.save()
    g.app.onQuit(event)
#@+node:ekr.20140804202802.18157: *3* :xa
@g.command(':xa') # same as wq
def vim_colon_xa(event):
    '''Save all open files and exit.'''
    for c in g.app.commanders():
        c.save()
    g.app.onQuit(event)
#@+node:ekr.20140804202802.18158: *3* not ready yet
if 0:
    #@+others
    #@+node:ekr.20140804202802.18159: *4* :e
    @g.command(':e') # :e directory name
    def colon_e(event):
        '''Open a file from a director list.'''
        c = event.get('c')
        if c:
            g.trace(':e not ready yet')
    #@+node:ekr.20140804202802.18153: *4* :tabnew
    @g.command(':tabnew') # :tabnew filename
    def colon_tabnew(event):
        '''Open a file in a new tab.'''
        c = event.get('c')
        if c:
            g.trace(':tabnew not ready yet')
    #@-others
#@+node:ekr.20140802183521.17997: ** show_stroke
def show_stroke(stroke):
    '''Return the best human-readable form of stroke.'''
    s = stroke.s if g.isStroke(stroke) else stroke
    d = {
        '\n':           r'\n',
        'Ctrl+Left':    'Ctrl+Left',
        'Ctrl+Right':   'Ctrl+Right',
        'Ctrl+r':       'Ctrl+r',
        'Down':         '<Dn>',
        'Escape':       '<Esc>',
        'Left':         '<Lt>',
        'Right':        '<Rt>',
        'Up':           '<Up>',
        'colon':        ':',
        'dollar':       '$',
        'period':       '.',
        'space':        ' ',
    }
    # g.trace(stroke,d.get(s,s))
    return d.get(s,s)
#@+node:ekr.20140802183521.17996: ** class VimEvent
class VimEvent:
    '''A class to contain the components of the dot.'''
    def __init__(self,stroke,w):
        '''ctor for the VimEvent class.'''
        self.char = '' # For Leo's core.
        self.stroke = stroke
        self.w = w
        self.widget = w # For Leo's core.
    def __repr__(self):
        '''Return the representation of the stroke.'''
        return show_stroke(self.stroke)
    __str__ = __repr__
#@+node:ekr.20131113045621.16547: ** class VimCommands
class VimCommands:
    '''A class that handles vim simulation in Leo.'''
    # pylint: disable=no-self-argument
    # The first argument is vc.
    #@+others
    #@+node:ekr.20131109170017.16507: *3*  vc.ctor & helpers
    def __init__(vc,c):
        '''The ctor for the VimCommands class.'''
        vc.c = c
        vc.k = c.k
        vc.init_constant_ivars()
        vc.init_dot_ivars()
        vc.init_persistent_ivars()
        vc.init_state_ivars()
        vc.create_dispatch_dicts()
    #@+node:ekr.20140805130800.18157: *4* dispatch dicts...
    #@+node:ekr.20140805130800.18162: *5* vc.create_dispatch_dicts
    def create_dispatch_dicts(vc):
        '''Create all dispatch dicts.'''
        vc.normal_mode_dispatch_d = d1 = vc.create_normal_dispatch_d()
            # Dispatch table for normal mode.
        vc.motion_dispatch_d = d2 = vc.create_motion_dispatch_d()
            # Dispatch table for motions.
        vc.vis_dispatch_d = d3 = vc.create_vis_dispatch_d()
            # Dispatch table for visual mode.
        # Add all entries in arrow dict to the other dicts.
        vc.arrow_d = arrow_d = vc.create_arrow_d()
        for d,tag in ((d1,'normal'),(d2,'motion'),(d3,'visual')):
            for key in arrow_d.keys():
                if key in d:
                    g.trace('duplicate arrow key in %s dict: %s' % (tag,key))
                else:
                    d[key] = arrow_d.get(key)
        if 1:
            # Check for conflicts between motion dict (d2) and the normal and visual dicts.
            # These are not necessarily errors, but are useful for debugging.
            for d,tag in ((d1,'normal'),(d3,'visual')):
                for key in d2.keys():
                    f,f2 = d.get(key),d2.get(key)
                    if f2 and f and f != f2:
                        g.trace('conflicting motion key in %s dict: %s %s %s' % (
                                tag,key,f2.__name__,f.__name__))
                    elif f2 and not f:
                        g.trace('missing motion key in %s dict: %s %s' % (
                            tag,key,f2.__name__))
                        # d[key] = f2
    #@+node:ekr.20140222064735.16702: *5* vc.create_motion_dispatch_d
    def create_motion_dispatch_d(vc):
        '''
        Return the dispatch dict for motions.
        Keys are strokes, values are methods.
        '''
        d = {
        'asciicircum': vc.vim_caret,# '^'
        'asciitilde': None,         # '~'
        'asterisk': None,           # '*'
        'at': None,                 # '@'
        'bar': None,                # '|'
        'braceleft': None,          # '{'
        'braceright': None,         # '}'
        'bracketleft': None,        # '['
        'bracketright': None,       # ']'
        'colon': None,              # ':' Not a motion.
        'comma': None,              # ','
        'dollar': vc.vim_dollar,    # '$'
        'greater': None,            # '>'
        'less': None,               # '<'
        'minus': None,              # '-'
        'numbersign': None,         # '#'
        'parenleft': None,          # '('
        'parenright': None,         # ')'
        'percent': None,            # '%'
        'period': None,             # '.' Not a motion.
        'plus': None,               # '+'
        'question': vc.vim_question,# '?'
        'quotedbl': None,           # '"'
        'quoteleft': None,          # '`'
        'Return':vc.vim_return,     # '\n'
        'semicolon': None,          # ';'
        'slash': vc.vim_slash,      # '/'
        'underscore': None,         # '_'
        # Digits.
        '0': vc.vim_0, # Only 0 starts a motion.
        # Uppercase letters.
        'A': None,  # vim doesn't enter insert mode.
        'B': None,
        'C': None,
        'D': None,
        'E': None,
        'F': vc.vim_F,
        'G': vc.vim_G,
        'H': None,
        'I': None,
        'J': None,
        'K': None,
        'L': None,
        'M': None,
        'N': None,
        'O': None,  # vim doesn't enter insert mode.
        'P': None,
        'R': None,
        'S': None,
        'T': vc.vim_T,
        'U': None,
        'V': None,
        'W': None,
        'X': None,
        'Y': vc.vim_Y, # Yank Leo outline.
        'Z': None,
        # Lowercase letters...
        'a': None,      # vim doesn't enter insert mode.
        'b': vc.vim_b,
        # 'c': vc.vim_c,
        'd': None,      # Not valid.
        'e': vc.vim_e,
        'f': vc.vim_f,
        'g': vc.vim_g,
        'h': vc.vim_h,
        'i': None,      # vim doesn't enter insert mode.
        'j': vc.vim_j,
        'k': vc.vim_k,
        'l': vc.vim_l,
        # 'm': vc.vim_m,
        # 'n': vc.vim_n,
        'o': None,      # vim doesn't enter insert mode.
        # 'p': vc.vim_p,
        # 'q': vc.vim_q,
        # 'r': vc.vim_r,
        # 's': vc.vim_s,
        't': vc.vim_t,
        # 'u': vc.vim_u,
        # 'v': vc.vim_v,
        'w': vc.vim_w,
        # 'x': vc.vim_x,
        # 'y': vc.vim_y,
        # 'z': vc.vim_z,
        }
        return d
    #@+node:ekr.20131111061547.16460: *5* vc.create_normal_dispatch_d
    def create_normal_dispatch_d(vc):
        '''
        Return the dispatch dict for normal mode.
        Keys are strokes, values are methods.
        '''
        d = {
        # Vim hard-coded control characters...
        # 'Ctrl+r': vc.vim_ctrl_r,
        # Special chars: these are the Leo's official (tk) strokes.
        'asciicircum': vc.vim_caret,# '^'
        'asciitilde': None,         # '~'
        'asterisk': vc.vim_star,    # '*'
        'at': None,                 # '@'
        'bar': None,                # '|'
        'braceleft': None,          # '{'
        'braceright': None,         # '}'
        'bracketleft': None,        # '['
        'bracketright': None,       # ']'
        'colon': vc.vim_colon,      # ':'
        'comma': None,              # ','
        'dollar': vc.vim_dollar,    # '$'
        'greater': None,            # '>'
        'less': None,               # '<'
        'minus': None,              # '-'
        'numbersign': vc.vim_pound, # '#'
        'parenleft': None,          # '('
        'parenright': None,         # ')'
        'percent': None,            # '%'
        'period': vc.vim_dot,       # '.'
        'plus': None,               # '+'
        'question': vc.vim_question,# '?'
        'quotedbl': None,           # '"'
        'quoteleft': None,          # '`'
        'Return':vc.vim_return,     # '\n'
        'semicolon': None,          # ';'
        'slash': vc.vim_slash,      # '/'
        'underscore': None,         # '_'
        # Digits.
        '0': vc.vim_0,
        '1': vc.vim_digits,
        '2': vc.vim_digits,
        '3': vc.vim_digits,
        '4': vc.vim_digits,
        '5': vc.vim_digits,
        '6': vc.vim_digits,
        '7': vc.vim_digits,
        '8': vc.vim_digits,
        '9': vc.vim_digits,
        # Uppercase letters.
        'A': vc.vim_A,
        'B': None,
        'C': None,
        'D': None,
        'E': None,
        'F': vc.vim_F,
        'G': vc.vim_G,
        'H': None,
        'I': None,
        'J': None,
        'K': None,
        'L': None,
        'M': None,
        'N': None,
        'O': vc.vim_O,
        'P': vc.vim_P, # Paste *outline*
        'R': None,
        'S': None,
        'T': vc.vim_T,
        'U': None,
        'V': vc.vim_V,
        'W': None,
        'X': None,
        'Y': vc.vim_Y,
        'Z': None,
        # Lowercase letters...
        'a': vc.vim_a,
        'b': vc.vim_b,
        'c': vc.vim_c,
        'd': vc.vim_d,
        'e': vc.vim_e,
        'f': vc.vim_f,
        'g': vc.vim_g,
        'h': vc.vim_h,
        'i': vc.vim_i,
        'j': vc.vim_j,
        'k': vc.vim_k,
        'l': vc.vim_l,
        'm': vc.vim_m,
        'n': vc.vim_n,
        'o': vc.vim_o,
        'p': vc.vim_p,
        'q': vc.vim_q,
        'r': vc.vim_r,
        's': vc.vim_s,
        't': vc.vim_t,
        'u': vc.vim_u,
        'v': vc.vim_v,
        'w': vc.vim_w,
        'x': vc.vim_x,
        'y': vc.vim_y,
        'z': vc.vim_z,
        }
        return d
    #@+node:ekr.20140222064735.16630: *5* vc.create_vis_dispatch_d
    def create_vis_dispatch_d (vc):
        '''
        Create a dispatch dict for visual mode.
        Keys are strokes, values are methods.
        '''
        d = {
        'Return':vc.vim_return,
        'space': vc.vim_l,
        # Terminating commands...
        'Escape': vc.vis_escape,
        'J': vc.vis_J,
        'c': vc.vis_c,
        'd': vc.vis_d,
        'u': vc.vis_u,
        'v': vc.vis_v,
        'y': vc.vis_y,
        # Motions...
        '0': vc.vim_0,
        '1': vc.vim_digits,
        '2': vc.vim_digits,
        '3': vc.vim_digits,
        '4': vc.vim_digits,
        '5': vc.vim_digits,
        '6': vc.vim_digits,
        '7': vc.vim_digits,
        '8': vc.vim_digits,
        '9': vc.vim_digits,
        'F': vc.vim_F,
        'G': vc.vim_G,
        'T': vc.vim_T,
        'Y': vc.vim_Y,
        'asciicircum': vc.vim_caret,
        'b': vc.vim_b,
        'dollar': vc.vim_dollar,
        'e': vc.vim_e,
        'f': vc.vim_f,
        'g': vc.vim_g,
        'h': vc.vim_h,
        'j': vc.vim_j,
        'k': vc.vim_k,
        'l': vc.vim_l,
        'n': vc.vim_n,
        'question': vc.vim_question,
        'slash': vc.vim_slash,
        't': vc.vim_t,
        'V': vc.vim_V,
        'w': vc.vim_w,
        }
        return d
    #@+node:ekr.20140805130800.18161: *5* vc.create_arrow_d
    def create_arrow_d(vc):
        '''Return a dict binding *all* arrows to vc.arrow.'''
        d = {}
        for arrow in ('Left','Right','Up','Down'):
            for mod in ('',
                'Alt+','Alt+Ctrl','Alt+Ctrl+Shift',
                'Ctrl+','Shift+','Ctrl+Shift+'
            ):
                d[mod+arrow] = vc.vim_arrow
        return d
    #@+node:ekr.20140804222959.18930: *4* vc.finshCreate
    def finishCreate(vc):
        '''Complete the initialization for the VimCommands class.'''
        # Set the widget for vc.set_border.
        c = vc.c
        if c.vim_mode:
            # g.registerHandler('idle',vc.on_idle)
            try:
                # Be careful: c.frame or c.frame.body may not exist in some gui's.
                vc.w = vc.c.frame.body.bodyCtrl
            except Exception:
                vc.w = None
            if c.config.getBool('vim-trainer-mode',default=False):
                vc.toggle_vim_trainer()
    #@+node:ekr.20140803220119.18103: *4* vc.init helpers
    # Every ivar of this class must be initied in exactly one init helper.
    #@+node:ekr.20140803220119.18104: *5* vc.init_dot_ivars
    def init_dot_ivars(vc):
        '''Init all dot-related ivars.'''
        vc.in_dot = False
            # True if we are executing the dot command.
        vc.dot_list = []
            # This list is preserved across commands.
        vc.old_dot_list = []
            # The dot_list saved at the start of visual mode.
    #@+node:ekr.20140803220119.18109: *5* vc.init_constant_ivars
    def init_constant_ivars(vc):
        '''Init ivars whose values never change.'''
        vc.chars = [ch for ch in string.printable if 32 <= ord(ch) < 128]
            # List of printable characters
        vc.register_names = string.ascii_letters
            # List of register names.
    #@+node:ekr.20140803220119.18106: *5* vc.init_state_ivars
    def init_state_ivars(vc):
        '''Init all ivars related to command state.'''
        vc.ch = None
            # The incoming character.
        vc.command_i = None
            # The offset into the text at the start of a command.
        vc.command_list = []
            # The list of all characters seen in this command.
        vc.command_n = None
            # The repeat count in effect at the start of a command.
        vc.command_w = None
            # The widget in effect at the start of a command.
        vc.event = None
            # The event for the current key.
        vc.extend = False
            # True: extending selection.
        vc.handler = vc.do_normal_mode
            # Use the handler for normal mode.
        vc.in_command = False
            # True: we have seen some command characters.
        vc.in_motion = False
            # True if parsing an *inner* motion, the 2j in d2j.
        vc.motion_func = None
            # The callback handler to execute after executing an inner motion.
        vc.motion_i = None
            # The offset into the text at the start of a motion.
        vc.n1 = 1
            # The first repeat count.
        vc.n = 1
            # The second repeat count.
        vc.n1_seen = False
            # True if vc.n1 has been set.
        vc.next_func = None
            # The continuation of a multi-character command.
        vc.old_sel = None
            # The selection range at the start of a command.
        vc.repeat_list = []
            # The characters of the current repeat count.
        vc.return_value = True
            # The value returned by vc.do_key.
            # Handlers set this to False to tell k.masterKeyHandler to handle the key.
        vc.state = 'normal'
            # in ('normal','insert','visual',)
        vc.stroke = None
            # The incoming stroke.
        vc.vis_mode_i = None
            # The insertion point at the start of visual mode.
        vc.vis_mode_w = None
            # The widget in effect at the start of visual mode.
    #@+node:ekr.20140803220119.18107: *5* vc.init_persistent_ivars
    def init_persistent_ivars(vc):
        '''Init ivars that are never re-inited.'''
        c = vc.c
        vc.colon_w = None
            # The widget that has focus when a ':' command begins.  May be None.
        vc.cross_lines = c.config.getBool('vim-crosses-lines',default=True)
            # True: allow f,F,h,l,t,T,x to cross line boundaries.
        vc.register_d = {}
            # Keys are letters; values are strings.
        vc.search_stroke = None
            # The stroke ('/' or '?') that starts a vim search command.
        vc.trainer = False
            # True: in vim-training mode:
            # Mouse clicks and arrows are disable.
        vc.w = None
            # The present widget.
            # c.frame.body.bodyCtrl is a QTextBrowser.
        vc.j_changed = True
            # False if the .leo file's change indicator should be
            # cleared after doing the j,j abbreviation.
    #@+node:ekr.20140803220119.18102: *4* vc.top-level inits
    # Called from command handlers or the ctor.
    #@+node:ekr.20140802225657.18023: *3* vc.acceptance methods
    # All acceptance methods must set vc.return_value.
    # All key handlers must end with a call to an acceptance method.
    #@+node:ekr.20140803220119.18097: *4* direct acceptance methods
    #@+node:ekr.20140802225657.18031: *5* vc.accept
    def accept(vc,add_to_dot=True,handler=None):
        '''
        Accept the present stroke.
        Optionally, this can set the dot or change vc.handler.
        This can be a no-op, but even then it is recommended.
        '''
        if handler:
            if vc.in_motion:
                # Tricky: queue up vc.do_inner_motion to continue the motion.
                vc.handler = vc.do_inner_motion
                vc.next_func = handler
            else:
                # Queue the outer handler as usual.
                vc.handler = handler
        if add_to_dot:
            vc.add_to_dot()
        vc.show_status()
        vc.return_value = True
    #@+node:ekr.20140802225657.18024: *5* vc.delegate
    def delegate(vc):
        '''Delegate the present key to k.masterKeyHandler.'''
        vc.show_status()
        vc.return_value = False
    #@+node:ekr.20140222064735.16631: *5* vc.done
    def done(vc,add_to_dot=True,return_value=True,set_dot=True,stroke=None):
        '''Complete a command, preserving text and optionally updating the dot.'''
        if vc.state == 'visual':
            vc.handler = vc.do_visual_mode
                # A major bug fix.
            if set_dot:
                stroke2 = stroke or vc.stroke if add_to_dot else None
                vc.compute_dot(stroke2)
            vc.command_list = []
            vc.show_status()
            vc.return_value = True
        else:
            if set_dot:
                stroke2 = stroke or vc.stroke if add_to_dot else None
                vc.compute_dot(stroke2)
            # Undoably preserve any changes to the body.
            vc.save_body()
            # Clear all state, enter normal mode & show the status.
            if vc.in_motion:
                vc.next_func = None
                # Do *not* change vc.in_motion!
            else:
                vc.init_state_ivars()
            vc.show_status()
            vc.return_value = return_value
    #@+node:ekr.20140802225657.18025: *5* vc.ignore
    def ignore(vc):
        '''Ignore the present key without passing it to k.masterKeyHandler.'''
        g.es('ignoring',vc.stroke,'in',vc.state,'mode',color='blue')
        g.trace(g.callers())
        vc.show_status()
        vc.return_value = True
    #@+node:ekr.20140806204042.18115: *5* vc.not_ready
    def not_ready(vc):
        '''Print a not ready message and quit.'''
        g.es('not ready',g.callers(1))
        vc.ignore()
            # More forgiving than quit. 
    #@+node:ekr.20140802120757.17999: *5* vc.quit
    def quit(vc):
        '''
        Abort any present command.
        Don't set the dot and enter normal mode.
        '''
        vc.state = 'normal'
        vc.done(return_value=True,set_dot=False,stroke=None)
    #@+node:ekr.20140807070500.18163: *5* vc.reset
    def reset(vc,setFocus):
        '''
        Called from k.keyboardQuit when the user types Ctrl-G (setFocus = True).
        Also called when the user clicks the mouse (setFocus = False).
        '''
        if setFocus:
            # A hard reset.
            vc.quit()
        else:
            # Do *not* change vc.state!
            pass
    #@+node:ekr.20140802225657.18034: *4* indirect acceptance methods
    #@+node:ekr.20140222064735.16709: *5* vc.begin_insert_mode
    def begin_insert_mode(vc,i=None,w=None):
        '''Common code for beginning insert mode.'''
        trace = False and not g.unitTesting
        c = vc.c
        if not w: w = vc.w
        vc.state = 'insert'
        vc.command_i = w.getInsertPoint() if i is None else i
        vc.command_w = w
        vc.accept(handler=vc.do_insert_mode,add_to_dot=False)
    #@+node:ekr.20140222064735.16706: *5* vc.begin_motion
    def begin_motion(vc,motion_func):
        '''Start an inner motion.'''
        # g.trace(motion_func.__name__,g.callers(2))
        w = vc.w
        vc.command_w = w
        vc.in_motion = True
        vc.motion_func = motion_func
        vc.motion_i = w.getInsertPoint()
        vc.n = 1
        if vc.stroke in '123456789':
            vc.vim_digits()
        else:
            vc.do_inner_motion()
    #@+node:ekr.20140801121720.18076: *5* vc.end_insert_mode
    def end_insert_mode(vc):
        '''End an insert mode started with the a,A,i,o and O commands.'''
        # Called from vim_esc.
        w = vc.w
        s = w.getAllText()
        i1 = vc.command_i
        i2 = w.getInsertPoint()
        if i1 > i2: i1,i2 = i2,i1
        s2 = s[i1:i2]
        if vc.n1 > 1:
            s3 = s2 * (vc.n1-1)
            g.trace(vc.in_dot,vc.n1,vc.n,s3)
            w.insert(i2,s3)
        for stroke in s2:
            vc.add_to_dot(stroke)
        vc.done()
    #@+node:ekr.20140222064735.16629: *5* vc.vim_digits
    def vim_digits(vc):
        '''Handle a digit that starts an outer repeat count.'''
        vc.repeat_list = []
        vc.repeat_list.append(vc.stroke)
        vc.accept(handler=vc.vim_digits_2)
            
    def vim_digits_2(vc):
        if vc.stroke in '0123456789':
            vc.repeat_list.append(vc.stroke)
            # g.trace('added',vc.stroke,vc.repeat_list)
            vc.accept(handler=vc.vim_digits_2)
        else:
            # Set vc.n1 before vc.n, so that inner motions won't repeat
            # until the end of vim mode.
            try:
                n = int(''.join(vc.repeat_list))
            except Exception:
                n = 1
            if vc.n1_seen:
                vc.n = n
            else:
                vc.n1_seen = True
                vc.n1 = n
            # Don't clear the repeat_list here.
            # The ending character may not be valid,
            if vc.in_motion:
                # Handle the stroke that ended the repeat count.
                vc.do_inner_motion(restart=True)
            else:
                # Restart the command.
                vc.do_normal_mode()
    #@+node:ekr.20131111061547.16467: *3* vc.commands
    #@+node:ekr.20140805130800.18158: *4* vc.arrow...
    def vim_arrow(vc):
        '''
        Handle all non-Alt arrows in any mode.
        This method attempts to leave focus unchanged.
        '''
        # pylint: disable=maybe-no-member
        s = vc.stroke.s if g.isStroke(vc.stroke) else vc.stroke
        if s.find('Alt+') > -1:
            # Any Alt key changes c.p.
            vc.quit()
            vc.delegate()
        elif vc.trainer:
            # Ignore all non-Alt arrow keys in text widgets.
            if vc.is_text_widget(vc.w):
                vc.ignore()
            else:
                # Allow plain-arrow keys work in the outline pane.
                vc.delegate()
        else:
            # Delegate all arrow keys.
            vc.delegate()
    #@+node:ekr.20140806075456.18152: *4* vc.vim_return
    def vim_return(vc):
        '''
        Handle a return key, regardless of mode.
        In the body pane only, it has special meaning.
        '''
        if vc.w:
            if vc.is_body(vc.w):
                if vc.state == 'normal':
                    vc.begin_insert_mode()
                elif vc.state == 'visual':
                    # same as v
                    vc.stroke = 'v'
                    vc.vis_v()
                else:
                    vc.done()
            else:
                vc.delegate()
        else:
            vc.delegate()
    #@+node:ekr.20140222064735.16634: *4* vc.vim...(normal mode)
    #@+node:ekr.20140810181832.18220: *5* vc.update_dot_before_search
    def update_dot_before_search(vc,find_pattern,change_pattern):
        '''A callback that updates the dot just before searching.'''
        # g.trace(vc.search_stroke,find_pattern,change_pattern)
        # Don't use vc.add_to_dot: it updates vc.command_list.
        def add(stroke):
            vc.dot_list.append(stroke)
        if vc.in_dot:
            # Don't set the dot again.
            return
        if vc.search_stroke is None:
            # We didn't start the search with / or ?
            return
        if 1:
            # This is all we can do until there is a substitution command.
            vc.change_pattern = change_pattern
                # Not used at present.
            add(vc.search_stroke)
            for ch in find_pattern:
                add(ch)
            vc.search_stroke = None
        else:
            # We could do this is we had a substitution command.
            if change_pattern is None:
                # A search pattern.
                add(vc.search_stroke)
                for ch in find_pattern:
                    add(ch)
            else:
                # A substitution:  :%s/find_pattern/change_pattern/g
                for s in (":%s/",find_pattern,"/",change_pattern,"/g"):
                    for ch in s:
                        add(ch)
            vc.search_stroke = None
    #@+node:ekr.20140811044942.18243: *5* vc.update_selection_after_search
    def update_selection_after_search(vc):
        '''Extend visual mode's selection after a search.'''
        if vc.state == 'visual':
            w = vc.w
            if w == g.app.gui.get_focus():
                i = w.getInsertPoint()
                w.setSelectionRange(vc.vis_mode_i,i,insert=i)
            else:
                g.trace('Search has changed nodes.')
    #@+node:ekr.20140221085636.16691: *5* vc.vim_0
    def vim_0(vc):
        '''Handle zero, either the '0' command or part of a repeat count.'''
        if vc.is_text_widget(vc.w):
            if vc.repeat_list:
                vc.vim_digits()
            else:
                if vc.state == 'visual':
                    vc.do('beginning-of-line-extend-selection')
                else:
                    vc.do('beginning-of-line')
                vc.done()
        elif vc.in_tree(vc.w):
            vc.do('goto-first-visible-node')
            vc.done()
        else:
            vc.quit()
    #@+node:ekr.20140220134748.16614: *5* vc.vim_a
    def vim_a(vc):
        '''Append text after the cursor N times.'''
        if vc.in_tree(vc.w):
            c = vc.c
            c.bodyWantsFocusNow()
            vc.w = w = c.frame.body.bodyCtrl
        else:
            w = vc.w
        if vc.is_text_widget(w):
            vc.do('forward-char')
            vc.begin_insert_mode()
        else:
            vc.quit()
    #@+node:ekr.20140730175636.17981: *5* vc.vim_A
    def vim_A(vc):
        '''Append text at the end the line N times.'''
        if vc.in_tree(vc.w):
            c = vc.c
            c.bodyWantsFocusNow()
            vc.w = w = c.frame.body.bodyCtrl
        else:
            w = vc.w
        if vc.is_text_widget(w):
            vc.do('end-of-line')
            vc.begin_insert_mode()
        else:
            vc.quit()
    #@+node:ekr.20140220134748.16618: *5* vc.vim_b
    def vim_b(vc):
        '''N words backward.'''
        if vc.is_text_widget(vc.w):
            for z in range(vc.n1*vc.n):
                if vc.state == 'visual':
                    vc.do('back-word-extend-selection')
                else:
                    vc.do('back-word')
            vc.done()
        else:
            vc.quit()
    #@+node:ekr.20140220134748.16619: *5* vc.vim_c (to do)
    def vim_c(vc):
        '''
        N   cc        change N lines
        N   c{motion} change the text that is moved over with {motion}
        VIS c         change the highlighted text
        '''
        vc.not_ready()
        ### vc.accept(handler=vc.vim_c2)
        
    def vim_c2(vc):
        if vc.is_text_widget(vc.w):
            g.trace(vc.stroke)
            vc.done()
        else:
            vc.quit()
    #@+node:ekr.20140807152406.18128: *5* vc.vim_caret
    def vim_caret(vc):
        '''Move to start of line.'''
        if vc.is_text_widget(vc.w):
            if vc.state == 'visual':
                vc.do('back-to-home-extend-selection')
            else:
                vc.do('back-to-home')
            vc.done()
        else:
            vc.quit()
    #@+node:ekr.20140730175636.17983: *5* vc.vim_colon
    def vim_colon(vc):
        '''Enter the minibuffer.'''
        k = vc.k
        vc.colon_w = vc.w # A scratch ivar, for :gt & gT commands.
        vc.quit()
        event = VimEvent(stroke='colon',w=vc.w)
        k.fullCommand(event=event)
        k.extendLabel(':')
    #@+node:ekr.20140806123540.18159: *5* vc.vim_comma (not used)
    # This was an attempt to be clever: two commas would switch to insert mode.
    def vim_comma(vc):
        '''Handle a comma in normal mode.'''
        if vc.is_text_widget(vc.w):
            vc.accept(handler=vc.vim_comma2)
        else:
            vc.quit()
        
    def vim_comma2(vc):
        if vc.is_text_widget(vc.w):
            if vc.stroke == 'comma':
                vc.begin_insert_mode()
            else:
                vc.done()
        else:
            vc.quit()
    #@+node:ekr.20140730175636.17992: *5* vc.vim_ctrl_r
    def vim_ctrl_r(vc):
        '''Redo the last command.'''
        vc.c.undoer.redo()
        vc.done()
    #@+node:ekr.20131111171616.16498: *5* vc.vim_d & helpers
    def vim_d(vc):
        '''
        N dd      delete N lines
        d{motion} delete the text that is moved over with {motion}
        '''
        if vc.is_text_widget(vc.w):
            vc.n = 1
            vc.accept(handler=vc.vim_d2)
        else:
            vc.quit()
        
    #@+node:ekr.20140811175537.18146: *6* vc.vim_d2
    def vim_d2(vc):
        '''Handle the second stroke of the d command.'''
        if vc.is_text_widget(vc.w):
            if vc.stroke == 'd':
                w = vc.w
                i = w.getInsertPoint()
                for z in range(vc.n1*vc.n):
                    # It's simplest just to get the text again.
                    s = w.getAllText()
                    i,j = g.getLine(s,i)
                    # Special case for end of buffer only for n == 1.
                    # This is exactly how vim works.
                    if vc.n1*vc.n == 1 and i == j == len(s):
                        i = max(0,i-1)
                    w.delete(i,j)
                vc.done()
            elif vc.stroke == 'i':
                vc.accept(handler=vc.vim_di)
            else:
                vc.d_stroke = vc.stroke # A scratch var.
                vc.begin_motion(vc.vim_d3)
        else:
            vc.quit()
    #@+node:ekr.20140811175537.18147: *6* vc.vim_d3
    def vim_d3(vc):
        '''Complete the d command after the cursor has moved.'''
        # d2w doesn't extend to line.  d2j does.
        trace = False and not g.unitTesting
        if vc.is_text_widget(vc.w):
            extend_to_line = vc.d_stroke in ('jk')
            w = vc.w
            s = w.getAllText()
            i1,i2 = vc.motion_i,w.getInsertPoint()
            if i1 == i2:
                if trace: g.trace('no change')
            elif i1 < i2:
                for z in range(vc.n1*vc.n):
                    if extend_to_line:
                        i2 = vc.to_eol(s,i2)
                        if i2 < len(s) and s[i2] == '\n':
                            i2 += 1
                        if trace: g.trace('extend i2 to eol',i1,i2)
                w.delete(i1,i2)
            else: # i1 > i2
                i1,i2 = i2,i1
                for z in range(vc.n1*vc.n):
                    if extend_to_line:
                        i1 = vc.to_bol(s,i1)
                        if trace: g.trace('extend i1 to bol',i1,i2)
                w.delete(i1,i2)
            vc.done()
        else:
            vc.quit()
    #@+node:ekr.20140811175537.18145: *6* vc.vim_di
    def vim_di(vc):
        '''Handle delete inner commands.'''
        if vc.is_text_widget(vc.w):
            if vc.stroke == 'w':
                # diw
                vc.do(['extend-to-word','backward-delete-char'])
                vc.done()
            else:
                vc.ignore()
                vc.quit()
        else:
            vc.quit()
    #@+node:ekr.20140730175636.17991: *5* vc.vim_dollar
    def vim_dollar(vc):
        '''Move the cursor to the end of the line.'''
        if vc.is_text_widget(vc.w):
            if vc.state == 'visual':
                vc.do('end-of-line-extend-selection')
            else:
                vc.do('end-of-line')
            vc.done()
        else:
            vc.quit()

    #@+node:ekr.20131111105746.16544: *5* vc.vim_dot
    def vim_dot(vc):
        '''Repeat the last command.'''
        try:
            vc.in_dot = True
            # Copy the list so it can't change in the loop.
            for event in vc.dot_list[:]:
                # g.trace(vc.state,event)
                vc.do_key(event)
        finally:
            vc.in_dot = False
        vc.done()
    #@+node:ekr.20140222064735.16623: *5* vc.vim_e
    def vim_e(vc):
        '''Forward to the end of the Nth word.'''
        if vc.is_text_widget(vc.w):
            for z in range(vc.n1*vc.n):
                if vc.state == 'visual':
                    vc.do('forward-word-extend-selection')
                else:
                    vc.do('forward-word')
            vc.done()
        elif vc.in_tree(vc.w):
            vc.do('goto-last-visible-node')
            vc.done()
        else:
            vc.quit()

    #@+node:ekr.20140222064735.16632: *5* vc.vim_esc
    def vim_esc(vc):
        '''
        Handle Esc while accumulating a normal mode command.

        Esc terminates the a,A,i,o and O commands normally.
        Call vc.end_insert command to support repeat counts
        such as 5a<lots of typing><esc>
        '''
        if vc.state == 'insert':
            vc.end_insert_mode()
        elif vc.state == 'visual':
            # Clear the selection and reset dot.
            vc.vis_v()
        else:
            # vc.done()
            vc.quit() # It's helpful to clear everything.
    #@+node:ekr.20140222064735.16687: *5* vc.vim_F
    def vim_F(vc):
        '''Back to the Nth occurrence of <char>.'''
        if vc.is_text_widget(vc.w):
            vc.accept(handler=vc.vim_F2)
        else:
            vc.quit()

    def vim_F2(vc):
        '''Handle F <stroke>'''
        if vc.is_text_widget(vc.w):
            w = vc.w
            s = w.getAllText()
            if s:
                i = i1 = w.getInsertPoint()
                match_i,n = None,vc.n1*vc.n
                i -= 1 # ensure progess.
                while i >= 0:
                    if s[i] == vc.ch:
                        match_i,n = i,n-1
                        if n == 0: break
                    elif s[i] == '\n' and not vc.cross_lines:
                        break
                    i -= 1
                if match_i is not None:
                    for z in range(i1-match_i-1):
                        if vc.state == 'visual':
                            vc.do('back-char-extend-selection')
                        else:
                            vc.do('back-char')
            vc.done()
        else:
            vc.quit()
    #@+node:ekr.20140220134748.16620: *5* vc.vim_f
    def vim_f(vc):
        '''move past the Nth occurrence of <stroke>.'''
        if vc.is_text_widget(vc.w):
            vc.accept(handler=vc.vim_f2)
        else:
            vc.quit()

    def vim_f2(vc):
        '''Handle f <stroke>'''
        trace = bool and not g.unitTesting
        if vc.is_text_widget(vc.w):
            ec = vc.c.editCommands
            w = vc.w
            s = w.getAllText()
            if s:
                i = i1 = w.getInsertPoint()
                match_i,n = None,vc.n1*vc.n
                while i < len(s):
                    if s[i] == vc.ch:
                        match_i,n = i,n-1
                        if n == 0: break
                    elif s[i] == '\n' and not vc.cross_lines:
                        break
                    i += 1
                if match_i is not None:
                    for z in range(match_i-i1+1):
                        if vc.state == 'visual':
                            vc.do('forward-char-extend-selection')
                        else:
                            vc.do('forward-char')
            vc.done()
        else:
            vc.quit()
    #@+node:ekr.20140803220119.18112: *5* vc.vim_G
    def vim_G(vc):
        '''Put the cursor on the last character of the file.'''
        if vc.is_text_widget(vc.w):
            if vc.state == 'visual':
                vc.do('end-of-buffer-extend-selection')
            else:
                vc.do('end-of-buffer')
            vc.done()
        else:
            vc.quit()
    #@+node:ekr.20140220134748.16621: *5* vc.vim_g
    def vim_g(vc):
        '''
        N ge backward to the end of the Nth word
        N gg goto line N (default: first line), on the first non-blank character
          gv start highlighting on previous visual area
        '''
        if vc.is_text_widget(vc.w):
            vc.accept(handler=vc.vim_g2)
        else:
            vc.quit()
        
    def vim_g2(vc):
        
        if vc.is_text_widget(vc.w):
            event,w = vc.event,vc.w
            extend = vc.state == 'visual'
            s = w.getAllText()
            i = w.getInsertPoint()
            if vc.stroke == 'g':
                # Go to start of buffer.
                on_line = vc.on_same_line(s,0,i)
                if on_line and extend:
                    vc.do('back-to-home-extend-selection')
                elif on_line:
                    vc.do('back-to-home')
                elif extend:
                    vc.do('beginning-of-buffer-extend-selection')
                else:
                    vc.do('beginning-of-buffer')
                vc.done()
            elif vc.stroke == 'b':
                # go to beginning of line: like 0.
                if extend:
                    vc.do('beginning-of-line-extend-selection')
                else:
                    vc.do('beginning-of-line')
                vc.done()
            elif vc.stroke == 'e':
                # got to end of line: like $
                if vc.state == 'visual':
                    vc.do('end-of-line-extend-selection')
                else:
                    vc.do('end-of-line')
                vc.done()
            elif vc.stroke == 'h':
                # go home: like ^.
                if extend:
                    vc.do('back-to-home-extend-selection')
                elif on_line:
                    vc.do('back-to-home')
                vc.done()
            else:
                vc.ignore()
                vc.done()
        else:
            vc.quit()

    #@+node:ekr.20131111061547.16468: *5* vc.vim_h
    def vim_h(vc):
        '''Move the cursor left n chars, but not out of the present line.'''
        trace = False and not g.unitTesting
        if vc.is_text_widget(vc.w):
            w = vc.w
            s = w.getAllText()
            i = w.getInsertPoint()
            if i == 0 or (i > 0 and s[i-1] == '\n'):
                if trace: g.trace('at line start')
            else:
                for z in range(vc.n1*vc.n):
                    if i > 0 and s[i-1] != '\n':
                        i -= 1
                    if i == 0 or (i > 0 and s[i-1] == '\n'):
                        break # Don't go past present line.
                if vc.state == 'visual':
                    w.setSelectionRange(vc.vis_mode_i,i,insert=i)
                else:
                    w.setInsertPoint(i)
            vc.done()
        elif vc.in_tree(vc.w):
            vc.do('contract-or-go-left')
            vc.done()
        else:
            vc.quit()
    #@+node:ekr.20140222064735.16618: *5* vc.vim_i
    def vim_i(vc):
        '''Insert text before the cursor N times.'''
        if vc.in_tree(vc.w):
            c = vc.c
            c.bodyWantsFocusNow()
            vc.w = w = c.frame.body.bodyCtrl
        else:
            w = vc.w
        if vc.is_text_widget(w):
            vc.begin_insert_mode()
        else:
            vc.done()

    #@+node:ekr.20140220134748.16617: *5* vc.vim_j
    def vim_j(vc):
        '''N j  Down n lines.'''
        if vc.is_text_widget(vc.w):
            for z in range(vc.n1*vc.n):
                if vc.state == 'visual':
                    vc.do('next-line-extend-selection')
                else:
                    vc.do('next-line')
            vc.done()
        elif vc.in_tree(vc.w):
            vc.do('goto-next-visible')
            vc.done()
        else:
            vc.quit()
    #@+node:ekr.20140222064735.16628: *5* vc.vim_k
    def vim_k(vc):
        '''Cursor up N lines.'''
        if vc.is_text_widget(vc.w):
            for z in range(vc.n1 * vc.n):
                if vc.state == 'visual':
                    vc.do('previous-line-extend-selection')
                else:
                    vc.do('previous-line')
            vc.done()
        elif vc.in_tree(vc.w):
            vc.do('goto-prev-visible')
            vc.done()
        else:
            vc.quit()
    #@+node:ekr.20140222064735.16627: *5* vc.vim_l
    def vim_l(vc):
        '''Move the cursor right vc.n chars, but not out of the present line.'''
        trace = False and not g.unitTesting
        if vc.is_text_widget(vc.w):
            w = vc.w
            s = w.getAllText()
            i = w.getInsertPoint()
            if i >= len(s) or s[i] == '\n':
                if trace: g.trace('at line end')
            else:
                for z in range(vc.n1*vc.n):
                    if i < len(s) and s[i] != '\n':
                        i += 1
                    if i >= len(s) or s[i] == '\n':
                        break # Don't go past present line.
                if vc.state == 'visual':
                    w.setSelectionRange(vc.vis_mode_i,i,insert=i)
                else:
                    w.setInsertPoint(i)
            vc.done()
        elif vc.in_tree(vc.w):
            vc.do('expand-and-go-right')
            vc.done()
        else:
            vc.quit()
    #@+node:ekr.20131111171616.16497: *5* vc.vim_m (to do)
    def vim_m(vc):
        '''m<a-zA-Z> mark current position with mark.'''
        vc.not_ready()
        ### vc.accept(handler=vc.vim_m2)
        
    def vim_m2(vc):
        g.trace(vc.stroke)
        vc.done()
    #@+node:ekr.20140220134748.16625: *5* vc.vim_n
    def vim_n(vc):
        '''Repeat last search N times.'''
        fc = vc.c.findCommands
        fc.setup_command()
        old_node_only = fc.node_only
        fc.node_only = True
        fc.findNext()
        vc.node_only = old_node_only
        vc.done()
    #@+node:ekr.20140222064735.16692: *5* vc.vim_O
    def vim_O(vc):
        '''Open a new line above the current line N times.'''
        if vc.in_tree(vc.w):
            c = vc.c
            c.bodyWantsFocusNow()
            vc.w = c.frame.body.bodyCtrl
        if vc.is_text_widget(vc.w):
            vc.do(['beginning-of-line','insert-newline','back-char'])
            vc.begin_insert_mode()
        else:
            vc.quit()
    #@+node:ekr.20140222064735.16619: *5* vc.vim_o
    def vim_o(vc):
        '''Open a new line below the current line N times.'''
        if vc.in_tree(vc.w):
            c = vc.c
            c.bodyWantsFocusNow()
            vc.w = w = c.frame.body.bodyCtrl
        else:
            w = vc.w
        if vc.is_text_widget(w):
            vc.do(['end-of-line','insert-newline'])
            vc.begin_insert_mode()
        else:
            vc.quit()
    #@+node:ekr.20140220134748.16622: *5* vc.vim_p
    def vim_p(vc):
        '''Paste after the cursor.'''
        if vc.in_tree(vc.w):
            vc.do('paste-node')
            vc.done()
        elif vc.is_text_widget(vc.w):
            vc.do('paste-text')
            vc.done()
        else:
            vc.quit()
    #@+node:ekr.20140807152406.18125: *5* vc.vim_P
    def vim_P(vc):
        '''Paste text at the cursor or paste a node before the present node.'''
        if vc.in_tree(vc.w):
            vc.do(['goto-prev-visible','paste-node'])
            vc.done()
        elif vc.is_text_widget(vc.w):
            vc.do(['back-char','paste-text'])
            vc.done()
        else:
            vc.quit()
    #@+node:ekr.20140808173212.18070: *5* vc.vim_pound
    def vim_pound(vc):
        '''Find previous occurance of word under the cursor.'''
        ec = vc.c.editCommands
        w = vc.w
        if vc.is_text_widget(w):
            i1 = w.getInsertPoint()
            if not w.hasSelection():
                vc.do('extend-to-word')
            if w.hasSelection():
                fc = vc.c.findCommands
                s = w.getSelectedText()
                w.setSelectionRange(i1,i1)
                if not vc.in_dot:
                    vc.dot_list.append(vc.stroke)
                old_node_only = fc.node_only
                fc.reverse = True
                fc.find_text = s
                fc.findNext()
                fc.reverse = False
                fc.node_only = old_node_only
            vc.done()
        else:
            vc.quit()
    #@+node:ekr.20140220134748.16623: *5* vc.vim_q (registers)
    def vim_q(vc):
        '''
        q       stop recording
        q<A-Z>  record typed characters, appended to register <a-z>
        q<a-z>  record typed characters into register <a-z>
        '''
        vc.not_ready()
        ### vc.accept(handler=vc.vim_q2)
        
    def vim_q2(vc):
        g.trace(vc.stroke)
        letters = string.ascii_letters
        vc.done()


    #@+node:ekr.20140807152406.18127: *5* vc.vim_question
    def vim_question(vc):
        '''Begin a search.'''
        if vc.is_text_widget(vc.w):
            fc = vc.c.findCommands
            ftm = fc.ftm
            vc.search_stroke = vc.stroke # A scratch ivar for vc.update_dot_before_search.
            fc.reverse = True
            fc.openFindTab(vc.event)
            fc.ftm.clear_focus()
            old_node_only = fc.node_only
            fc.searchWithPresentOptions(vc.event)
                # This returns immediately, before the actual search.
                # leoFind.showSuccess calls vc.update_selection_after_search.
            fc.node_only = old_node_only
            vc.done(add_to_dot=False,set_dot=False)
        else:
            vc.quit()
    #@+node:ekr.20140220134748.16624: *5* vc.vim_r (to do)
    def vim_r(vc):
        '''Replace next N characters with <char>'''
        vc.not_ready()
        ### vc.accept(handler=vc.vim_r2)
        
    def vim_r2(vc):
        g.trace(vc.n,vc.stroke)
        vc.done()
    #@+node:ekr.20140222064735.16625: *5* vc.vim_redo (to do)
    def vim_redo(vc):
        '''N Ctrl-R redo last N changes'''
        vc.not_ready()
    #@+node:ekr.20140222064735.16626: *5* vc.vim_s (to do)
    def vim_s(vc):
        '''Change N characters'''
        vc.not_ready()
        ### vc.accept(handler=vc.vim_s2)
        
    def vim_s2(vc):
        g.trace(vc.n,vc.stroke)
        vc.done()
    #@+node:ekr.20140222064735.16622: *5* vc.vim_slash
    def vim_slash(vc):
        '''Begin a search.'''
        if vc.is_text_widget(vc.w):
            fc = vc.c.findCommands
            vc.search_stroke = vc.stroke # A scratch ivar for vc.update_dot_before_search.
            fc.reverse = False
            fc.openFindTab(vc.event)
            fc.ftm.clear_focus()
            old_node_only = fc.node_only
            fc.searchWithPresentOptions(vc.event)
                # This returns immediately, before the actual search.
                # leoFind.showSuccess calls vc.update_selection_after_search.
            fc.node_only = old_node_only
            fc.reverse = False
            vc.done(add_to_dot=False,set_dot=False)
        else:
            vc.quit()
    #@+node:ekr.20140810210411.18239: *5* vc.vim_star
    def vim_star(vc):
        '''Find previous occurance of word under the cursor.'''
        ec = vc.c.editCommands
        w = vc.w
        if vc.is_text_widget(w):
            i1 = w.getInsertPoint()
            if not w.hasSelection():
                vc.do('extend-to-word')
            if w.hasSelection():
                fc = vc.c.findCommands
                s = w.getSelectedText()
                w.setSelectionRange(i1,i1)
                if not vc.in_dot:
                    vc.dot_list.append(vc.stroke)
                old_node_only = fc.node_only
                fc.reverse = False
                fc.find_text = s
                fc.findNext()
                fc.node_only = old_node_only
            vc.done()
        else:
            vc.quit()
    #@+node:ekr.20140222064735.16620: *5* vc.vim_t
    def vim_t(vc):
        '''Move before the Nth occurrence of <char> to the right.'''
        if vc.is_text_widget(vc.w):
            vc.accept(handler=vc.vim_t2)
        else:
            vc.quit()
        
    def vim_t2(vc):
        '''Handle t <stroke>'''
        if vc.is_text_widget(vc.w):
            ec = vc.c.editCommands
            w = vc.w
            s = w.getAllText()
            if s:
                i = i1 = w.getInsertPoint()
                match_i,n = None,vc.n1*vc.n
                while i < len(s):
                    if s[i] == vc.ch:
                        match_i,n = i,n-1
                        if n == 0: break
                    elif s[i] == '\n' and not vc.cross_lines:
                        break
                    i += 1
                if match_i is not None:
                    for z in range(match_i-i1):
                        if vc.state == 'visual':
                            vc.do('forward-char-extend-selection')
                        else:
                            vc.do('forward-char')
            vc.done()
        else:
            vc.quit()

    #@+node:ekr.20140222064735.16686: *5* vc.vim_T
    def vim_T(vc):
        '''Back before the Nth occurrence of <char>.'''
        if vc.is_text_widget(vc.w):
            vc.accept(handler=vc.vim_T2)
        else:
            vc.quit()

    def vim_T2(vc):
        '''Handle T <stroke>'''
        if vc.is_text_widget(vc.w):
            ec = vc.c.editCommands
            w = vc.w
            s = w.getAllText()
            if s:
                i = i1 = w.getInsertPoint()
                if i > 0 and s[i-1] == vc.ch:
                    i -= 1 # ensure progess.
                match_i,n = None,vc.n1*vc.n
                i -= 1
                while i >= 0:
                    if s[i] == vc.ch:
                        match_i,n = i,n-1
                        if n == 0: break
                    elif s[i] == '\n' and not vc.cross_lines:
                        break
                    i -= 1
                if match_i is not None:
                    # g.trace(i1-match_i,vc.ch)
                    for z in range(i1-match_i):
                        if vc.state == 'visual':
                            vc.do('back-char-extend-selection')
                        else:
                            vc.do('back-char')
            vc.done()
        else:
            vc.quit()

    #@+node:ekr.20140220134748.16626: *5* vc.vim_u
    def vim_u(vc):
        '''U undo the last command.'''
        vc.c.undoer.undo()
        vc.quit()
    #@+node:ekr.20140220134748.16627: *5* vc.vim_v
    def vim_v(vc):
        '''Start visual mode.'''
        if vc.n1_seen:
            vc.ignore()
            # vc.beep('%sv not valid' % vc.n1)
            # vc.done()
        elif vc.is_text_widget(vc.w):
            vc.vis_mode_w = w = vc.w
            vc.vis_mode_i = w.getInsertPoint()
            vc.state = 'visual'
            # Save the dot list in case v terminates visual mode.
            vc.old_dot_list = vc.dot_list[:]
            vc.accept(add_to_dot=False,handler=vc.do_visual_mode)
        else:
            vc.quit()
    #@+node:ekr.20140811110221.18250: *5* vc.vim_V
    def vim_V(vc):
        '''Visually select line.'''
        if vc.is_text_widget(vc.w):
            if vc.state == 'visual':
                bx = 'beginning-of-line-extend-selection'
                ex = 'end-of-line-extend-selection'
                s = vc.w.getAllText()
                i = vc.w.getInsertPoint()
                if vc.on_same_line(s,i,vc.vis_mode_i):
                    vc.do([bx,ex])
                else:
                    vc.do(ex if vc.vis_mode_i < i else bx)
            else:
                vc.do([bx,ex])
            vc.done()
        else:
            vc.quit()
    #@+node:ekr.20140222064735.16624: *5* vc.vim_w
    def vim_w(vc):
        '''N words forward.'''
        if vc.is_text_widget(vc.w):
            for z in range(vc.n1*vc.n):
                if vc.state == 'visual':
                    vc.do('forward-word-extend-selection')
                else:
                    vc.do('forward-word')
            vc.done()
        else:
            vc.quit()
        
    #@+node:ekr.20140220134748.16629: *5* vc.vim_x
    def vim_x(vc):
        '''Delete N characters under and after the cursor.'''
        w = vc.w
        if vc.is_text_widget(w):
            for z in range(vc.n1*vc.n):
                # It's simplest just to get the text again.
                s = w.getAllText()
                i = w.getInsertPoint()
                if i > 0:
                    if vc.cross_lines or s[i-1] != '\n':
                        w.delete(i-1,i)
                else:
                    break
            vc.done()
        else:
            vc.quit()
    #@+node:ekr.20140220134748.16630: *5* vc.vim_y
    def vim_y(vc):
        '''
        N   yy          yank N lines 
        N   y{motion}   yank the text moved over with {motion} 
        '''
        if vc.is_text_widget(vc.w):
            vc.accept(handler=vc.vim_y2)
        elif vc.in_tree(vc.w):
            # Paste an outline.
            c = vc.c
            g.es('Yank outline: %s' % c.p.h)
            c.copyOutline()
            vc.done()
        else:
            vc.quit()
        
    def vim_y2(vc):
        if vc.is_text_widget(vc.w):
            if vc.stroke == 'y':
                # Yank n lines.
                w = vc.w
                i1 = i = w.getInsertPoint()
                s = w.getAllText()
                for z in range(vc.n1*vc.n):
                    i,j = g.getLine(s,i) 
                    i = j + 1
                w.setSelectionRange(i1,j,insert=j)
                vc.c.frame.copyText(event=vc.event)
                w.setInsertPoint(i1)
                vc.done()
            else:
                vc.y_stroke = vc.stroke # A scratch var.
                vc.begin_motion(vc.vim_y3)
        else:
            vc.quit()
                
    def vim_y3(vc):
        '''Complete the y command after the cursor has moved.'''
        # The motion is responsible for all repeat counts.
         # y2w doesn't extend to line.  y2j does.
        trace = True and not g.unitTesting
        if vc.is_text_widget(vc.w):
            extend_to_line = vc.y_stroke in ('jk')
            n = vc.n1*vc.n
            w = vc.w
            s = w.getAllText()
            i1,i2 = vc.motion_i,w.getInsertPoint()
            if i1 == i2:
                if trace: g.trace('no change')
            elif i1 < i2:
                if extend_to_line:
                    i2 = vc.to_eol(s,i2)
                    if i2 < len(s) and s[i2] == '\n':
                        i2 += 1
                    if trace: g.trace('extend i2 to eol',i1,i2)
            else: # i1 > i2
                i1,i2 = i2,i1
                if extend_to_line:
                    i1 = vc.to_bol(s,i1)
                    if trace: g.trace('extend i1 to bol',i1,i2)
            if i1 != i2:
                # g.trace(repr(s[i1:i2]))
                w.setSelectionRange(i1,i2,insert=i2)
                vc.c.frame.copyText(event=vc.event)
                w.setInsertPoint(vc.motion_i)
            vc.done()
        else:
            vc.quit()
    #@+node:ekr.20140807152406.18126: *5* vc.vim_Y
    def vim_Y(vc):
        '''Yank a Leo outline.'''
        vc.not_ready()
    #@+node:ekr.20140220134748.16631: *5* vc.vim_z (to do)
    def vim_z(vc):
        '''
        zb redraw current line at bottom of window
        zz redraw current line at center of window
        zt redraw current line at top of window
        '''
        vc.not_ready()
        ### vc.accept(handler=vc.vim_z2)

    def vim_z2(vc):
        g.trace(vc.stroke)
        vc.done()
    #@+node:ekr.20140222064735.16658: *4* vc.vis_...(motions) (just notes)
    #@+node:ekr.20140801121720.18071: *5*  Notes
    #@@nocolor-node
    #@+at
    # Not yet:
    #     
    # N   B               (motion) N blank-separated WORDS backward
    # N   E               (motion) forward to the end of the Nth blank-separated WORD
    # N   G               (motion) goto line N (default: last line), on the first non-blank character
    # N   N               (motion) repeat last search, in opposite direction
    # N   W               (motion) N blank-separated WORDS forward
    # N   g#              (motion) like "#", but also find partial matches
    # N   g$              (motion) to last character in screen line (differs from "$" when lines wrap)
    # N   g*              (motion) like "*", but also find partial matches
    # N   g0              (motion) to first character in screen line (differs from "0" when lines wrap)
    #     gD              (motion) goto global declaration of identifier under the cursor
    # N   gE              (motion) backward to the end of the Nth blank-separated WORD
    #     gd              (motion) goto local declaration of identifier under the cursor
    # N   ge              (motion) backward to the end of the Nth word
    # N   gg              (motion) goto line N (default: first line), on the first non-blank character
    # N   gj              (motion) down N screen lines (differs from "j" when line wraps)
    # N   gk              (motion) up N screen lines (differs from "k" when line wraps)
    #@+node:ekr.20140222064735.16635: *5* motion non-letters (to do)
    #@@nocolor-node
    #@+at
    # 
    # First:
    # 
    #     0               (motion) to first character in the line (also: <Home> key)
    # N   $               (motion) go to the last character in the line (N-1 lines lower) (also: <End> key)
    #     ^               (motion) go to first non-blank character in the line
    # N   ,               (motion) repeat the last "f", "F", "t", or "T" N times in opposite direction
    # N   ;               (motion) repeat the last "f", "F", "t", or "T" N times
    # N   /<CR>                       (motion) repeat last search, in the forward direction
    # N   /{pattern}[/[offset]]<CR>   (motion) search forward for the Nth occurrence of {pattern}
    # N   ?<CR>                       (motion) repeat last search, in the backward direction
    # N   ?{pattern}[?[offset]]<CR>   (motion) search backward for the Nth occurrence of {pattern}
    # 
    # Later or never:
    #     
    # N   CTRL-I          (motion) go to Nth newer position in jump list
    # N   CTRL-O          (motion) go to Nth older position in jump list
    # N   CTRL-T          (motion) Jump back from Nth older tag in tag list
    #     
    # N   +               (motion) down N lines, on the first non-blank character (also: CTRL-M and <CR>)
    # N   _               (motion) down N-1 lines, on the first non-blank character
    # N   -               (motion) up N lines, on the first non-blank character
    # 
    # N   (               (motion) N sentences backward
    # N   )               (motion) N sentences forward
    # N   {               (motion) N paragraphs backward
    # N   }               (motion) N paragraphs forward
    # N   |               (motion) to column N (default: 1)
    #     `"              (motion) go to the position when last editing this file
    #     '<a-zA-Z0-9[]'"<>>  (motion) same as `, but on the first non-blank in the line
    #     `<              (motion) go to the start of the (previous) Visual area
    #     `<0-9>          (motion) go to the position where Vim was last exited
    #     `<A-Z>          (motion) go to mark <A-Z> in any file
    #     `<a-z>          (motion) go to mark <a-z> within current file
    #     `>              (motion) go to the end of the (previous) Visual area
    #     `[              (motion) go to the start of the previously operated or put text
    #     `]              (motion) go to the end of the previously operated or put text
    #     ``              (motion) go to the position before the last jump
    # 
    # N   %       (motion) goto line N percentage down in the file.  N must be given, otherwise it is the % command.
    #     %       (motion) find the next brace, bracket, comment, or "#if"/ "#else"/"#endif" in this line and go to its match
    # 
    # N   #       (motion) search backward for the identifier under the cursor
    # N   *       (motion) search forward for the identifier under the cursor
    # 
    # N   [#      (motion) N times back to unclosed "#if" or "#else"
    # N   [(      (motion) N times back to unclosed '('
    # N   [*      (motion) N times back to start of comment "/*"
    # N   [[      (motion) N sections backward, at start of section
    # N   []      (motion) N sections backward, at end of section
    # N   [p      (motion?) like P, but adjust indent to current line
    # N   [{      (motion) N times back to unclosed '{'
    # N   ]#      (motion) N times forward to unclosed "#else" or "#endif"
    # N   ])      (motion) N times forward to unclosed ')'
    # N   ]*      (motion) N times forward to end of comment "*/"
    # N   ][      (motion) N sections forward, at end of section
    # N   ]]      (motion) N sections forward, at start of section
    # N   ]p      (motion?) like p, but adjust indent to current line
    # N   ]}      (motion) N times forward to unclosed '}'
    #@+node:ekr.20140222064735.16655: *6* vis_minus
    #@+node:ekr.20140222064735.16654: *6* vis_plus
    #@+node:ekr.20140222064735.16647: *4* vc.vis_...(terminators)
    # Terminating commands call vc.done().
    #@+node:ekr.20140222064735.16684: *5* vis_escape
    def vis_escape(vc):
        '''Handle Escape in visual mode.'''
        vc.state = 'normal'
        vc.done()
    #@+node:ekr.20140222064735.16661: *5* vis_J
    def vis_J(vc):
        '''Join the highlighted lines.'''
        vc.state = 'normal'
        vc.not_ready()
        ### vc.done(set_dot=True)
    #@+node:ekr.20140222064735.16656: *5* vis_c (to do)
    def vis_c(vc):
        '''Change the highlighted text.'''
        vc.state = 'normal'
        vc.not_ready()
        ### vc.done(set_dot=True)
    #@+node:ekr.20140222064735.16657: *5* vis_d
    def vis_d(vc):
        '''Delete the highlighted text and terminate visual mode.'''
        w  = vc.vis_mode_w
        if vc.is_text_widget(w):
            i1 = vc.vis_mode_i
            i2 = w.getInsertPoint()
            w.delete(i1,i2)
            vc.state = 'normal'
            vc.done(set_dot=True)
        else:
            vc.quit()
    #@+node:ekr.20140222064735.16659: *5* vis_u
    def vis_u(vc):
        '''Make highlighted text lowercase.'''
        vc.state = 'normal'
        vc.not_ready()
        ### vc.done(set_dot=True)
    #@+node:ekr.20140222064735.16681: *5* vis_v
    def vis_v(vc):
        '''End visual mode.'''
        if 1:
            # End visual node, retain the selection, and set the dot.
            # This makes much more sense in Leo.
            vc.state = 'normal'
            vc.done()
        else:
            # The real vim clears the selection.
            w = vc.w
            if vc.is_text_widget(w):
                i = w.getInsertPoint()
                w.setSelectionRange(i,i)
                # Visual mode affects the dot only if there is a terminating command.
                vc.dot_list = vc.old_dot_list
                vc.state = 'normal'
                vc.done(set_dot=False)
    #@+node:ekr.20140222064735.16660: *5* vis_y
    def vis_y(vc):
        '''Yank the highlighted text.'''
        if vc.is_text_widget(vc.w):
            vc.c.frame.copyText(event=vc.event)
            vc.state = 'normal'
            vc.done(set_dot=True)
        else:
            vc.quit()

    #@+node:ekr.20140221085636.16685: *3* vc.do_key & helpers
    def do_key(vc,event):
        '''
        Handle the next key in vim mode:
        - Set vc.event, vc.w, vc.stroke and vc.ch for *all* handlers.
        - Call vc.handler.
        Return True if k.masterKeyHandler should handle this key.
        '''
        trace = False and not g.unitTesting
        vc.init_scanner_vars(event)
        if trace: g.trace('stroke: %s' % vc.stroke)
        vc.return_value = None
        if not vc.handle_specials():
            vc.handler()
        if vc.return_value not in (True,False):
            # It looks like no acceptance method has been called.
            vc.oops('bad return_value: %s %s %s' % (
                repr(vc.return_value),vc.state,vc.next_func))
            vc.done() # Sets vc.return_value to True.
        return vc.return_value
    #@+node:ekr.20140802225657.18021: *4* vc.handle_specials
    def handle_specials(vc):
        '''Return True vc.stroke is an Escape or a Return in the outline pane.'''
        if vc.stroke == 'Escape':
            # k.masterKeyHandler handles Ctrl-G.
            # Escape will end insert mode.
            vc.vim_esc()
            return True
        elif vc.stroke == 'Return' and vc.in_headline(vc.w):
            # End headline editing and enter normal mode.
            vc.c.endEditing()
            vc.done()
            return True
        else:
            return False
    #@+node:ekr.20140802120757.18003: *4* vc.init_scanner_vars
    def init_scanner_vars(vc,event):
        '''Init all ivars used by the scanner.'''
        assert event
        vc.event = event
        stroke = event.stroke
        vc.ch = event.char # Required for f,F,t,T.
        vc.stroke = stroke.s if g.isStroke(stroke) else stroke
        vc.w = event and event.w
        if not vc.in_command:
            vc.in_command = True # May be cleared later.
            if vc.is_text_widget(vc.w):
                vc.old_sel = vc.w.getSelectionRange()
    #@+node:ekr.20140808142143.18072: *3* vc.external commands
    #@+node:ekr.20140811173921.18142: *4* vc.cycle_focus & cycle_all_focus (:gt & :gT)
    def cycle_focus(vc):
        '''Cycle focus'''
        event = VimEvent(stroke='',w=vc.colon_w)
        vc.do('cycle-focus',event=event)
        
    def cycle_all_focus(vc):
        '''Cycle all focus'''
        event = VimEvent(stroke='',w=vc.colon_w)
        vc.do('cycle-all-focus',event=event)
    #@+node:ekr.20140811211944.18162: *4* vc.load_file_at_cursor (:r)
    def load_file_at_cursor(vc,event=None):
        '''Prompt for a file name, then load it at the cursor.'''
        vc.k.getFileName(event,callback=vc.r_callback)

    def r_callback(vc,fn):
        c,w = vc.c,vc.colon_w
        if not vc.is_text_widget(w):
            w = c.frame.body.bodyCtrl
        if g.os_path_exists(fn):
            f = open(fn)
            s = f.read()
            f.close()
            i = w.getInsertPoint()
            w.insert(i,s)
            vc.save_body()
        else:
            g.es('does not exist:' % fn)
    #@+node:ekr.20140810181832.18223: *4* vc.print_dot
    def print_dot(vc):
        '''Print the dot.'''
        try:
            i = 0
            aList = [vc.c.k.stroke2char(s) for s in vc.dot_list]
            while i < len(aList):
                g.es(','.join(aList[i:i+10]))
                i += 10
        except Exception:
            for z in vc.dot_list:
                g.es(repr(z))
    #@+node:ekr.20140811180848.18154: *4* vc.shell_command (:!)
    def shell_command(vc):
        '''Execute a shell command.'''
        event = VimEvent(stroke='',w=vc.colon_w)
        vc.do('shell-command',event=event)
    #@+node:ekr.20140811180848.18152: *4* vc.substitution (:%)
    def substitution(vc,leadin):
        '''
        Handle :%s/text/replaced text/g
        The lead-in characters :%s are in the minibuffer.
        '''
        g.trace(leadin)
    #@+node:ekr.20140811211944.18165: *4* vc.tabnew
    def tabnew(vc,event=None):
        '''
        Prompts for a file name.
        If the file exits, opens it in a new tab.
        Otherwise, opens a tab for a new file.
        '''
        vc.k.getFileName(event,callback=vc.tabnew_callback)

    def tabnew_callback(vc,fn):
        c = vc.c
        if fn and not g.os_path_isdir(fn):
            c2 = g.openWithFileName(fn,old_c=c)
            try:
                g.app.gui.runAtIdle(c2.treeWantsFocusNow)
            except Exception:
                pass
        else:
            c.new()
    #@+node:ekr.20140808142143.18075: *4* vc.toggle_vim_mode
    def toggle_vim_mode(vc):
        '''toggle vim-mode.'''
        c = vc.c
        c.vim_mode = not c.vim_mode
        g.es('vim-mode: %s' % (
            'on' if c.vim_mode else 'off'),
            color = 'red')
        if c.vim_mode:
            vc.quit()
        else:
            try:
                vc.state = 'insert'
                c.bodyWantsFocusNow()
                w = c.frame.body.bodyCtrl.widget
                vc.set_border(kind=None,w=w,activeFlag=True)
            except Exception:
                # g.es_exception()
                pass
    #@+node:ekr.20140808142143.18074: *4* vc.toggle_vim_trainer
    def toggle_vim_trainer(vc):
        '''toggle vim-trainer mode.'''
        vc.trainer = not vc.trainer
        g.es('vim-trainer-mode: %s' % (
            'on' if vc.trainer else 'off'),
            color = 'red')
    #@+node:ekr.20140802225657.18026: *3* vc.state handlers
    # Neither state handler nor key handlers ever return non-None.
    #@+node:ekr.20140803220119.18089: *4* vc.do_inner_motion
    def do_inner_motion(vc,restart=False):
        '''Handle strokes in motions.'''
        trace = False and not g.unitTesting
        if trace: g.trace(vc.command_list)
        assert vc.in_motion
        if restart:
            vc.next_func = None
        func = vc.next_func or vc.motion_dispatch_d.get(vc.stroke)
        if func:
            func()
            if vc.motion_func:
                vc.motion_func()
                vc.in_motion = False # Required.
                vc.done()
        elif vc.is_plain_key(vc.stroke):
            vc.ignore()
        else:
            # Pass non-plain keys to k.masterKeyHandler
            vc.delegate()

    #@+node:ekr.20140803220119.18090: *4* vc.do_insert_mode & helper
    def do_insert_mode(vc):
        '''Handle insert mode: delegate all strokes to k.masterKeyHandler.'''
        # Support the jj abbreviation when there is no selection.
        vc.state = 'insert'
        w = vc.w
        if vc.is_text_widget(w) and vc.test_for_insert_escape(w):
            return
        # Special case for arrow keys.
        if vc.stroke in vc.arrow_d:
            vc.vim_arrow()
        else:
            vc.delegate()

    #@+node:ekr.20140807112800.18122: *5* vc.test_for_insert_escape
    def test_for_insert_escape(vc,w):
        '''Return True if the j,j escape sequence has ended insert mode.'''
        c = vc.c
        s = w.getAllText()
        i = w.getInsertPoint()
        i2,j = w.getSelectionRange()
        if i2 == j and vc.stroke == 'j':
            if i > 0 and s[i-1] == 'j':
                # g.trace(i,i2,j,s[i-1:i+1])
                w.delete(i-1,i)
                w.setInsertPoint(i-1)
                # A benign hack: simulate an Escape for the dot.
                vc.stroke = 'Escape'
                vc.end_insert_mode()
                if not vc.j_changed:
                    c.setChanged(False)
                return True
            else:
                # Remember the changed state when we saw the first 'j'.
                vc.j_changed = c.isChanged()
        return False
    #@+node:ekr.20140803220119.18091: *4* vc.do_normal_mode
    def do_normal_mode(vc):
        '''Handle strokes in normal mode.'''
        # Unlike visual mode, there is no need to init anything,
        # because all normal mode commands call vc.done.
        vc.do_state(vc.normal_mode_dispatch_d,'normal')
        
    #@+node:ekr.20140802225657.18029: *4* vc.do_state
    def do_state(vc,d,mode_name):
        '''General dispatcher code. d is a dispatch dict.'''
        trace = False and not g.unitTesting
        func = d.get(vc.stroke)
        if func:
            if trace: g.trace(mode_name,vc.stroke,func.__name__)
            func()
        elif vc.is_plain_key(vc.stroke):
            if trace: g.trace('ignore',vc.stroke)
            vc.ignore()
        else:
            # Pass non-plain keys to k.masterKeyHandler
            if trace: g.trace('delegate',vc.stroke)
            vc.delegate()
    #@+node:ekr.20140803220119.18092: *4* vc.do_visual_mode
    def do_visual_mode(vc):
        '''Handle strokes in visual mode.'''
        vc.n1 = vc.n = 1
        vc.do_state(vc.vis_dispatch_d,'visual')
    #@+node:ekr.20140222064735.16682: *3* vc.Utilities
    #@+node:ekr.20140802142132.17981: *4* show_dot & show_list
    def show_command(vc):
        '''Show the accumulating command.'''
        return ''.join([repr(z) for z in vc.command_list])

    def show_dot(vc):
        '''Show the dot.'''
        s = ''.join([repr(z) for z in vc.dot_list[:10]])
        if len(vc.dot_list) > 10:
            s = s + '...'
        return s
    #@+node:ekr.20140802183521.17998: *4* vc.add_to_dot
    def add_to_dot(vc,stroke=None):
        '''
        Add a new VimEvent to vc.command_list.
        Never change vc.command_list if vc.in_dot is True
        Never add . to vc.command_list
        '''
        if not vc.in_dot:
            s = stroke or vc.stroke
            # Never add '.' to the dot list.
            if s and s != 'period':
                # g.trace(s)
                event = VimEvent(s,vc.w)
                vc.command_list.append(event)
    #@+node:ekr.20140802120757.18002: *4* vc.compute_dot
    def compute_dot(vc,stroke):
        '''Compute the dot and set vc.dot.'''
        if stroke:
            vc.add_to_dot(stroke)
        if vc.command_list:
            vc.dot_list = vc.command_list[:]
    #@+node:ekr.20140810214537.18241: *4* vc.do
    def do(vc,o,event=None):
        '''Do one or more Leo commands by name.'''
        if not event:
            event = vc.event
        if isinstance(o,(tuple,list)):
            for z in o:
                vc.c.k.simulateCommand(z,event=event)
        else:
            vc.c.k.simulateCommand(o,event=event)
    #@+node:ekr.20140802183521.17999: *4* vc.in_headline & vc.in_tree
    def in_headline(vc,w):
        '''Return True if we are in a headline edit widget.'''
        return vc.widget_name(w).startswith('head')

    def in_tree(vc,w):
        '''Return True if we are in the outline pane, but not in a headline.'''
        return vc.widget_name(w).startswith('canvas')
    #@+node:ekr.20140806081828.18157: *4* vc.is_body & is_head
    def is_body(vc,w):
        '''Return True if w is the QTextBrowser of the body pane.'''
        w2 = vc.c.frame.body.bodyCtrl
        return w == w2

    def is_head(vc,w):
        '''Return True if w is an headline edit widget.'''
        return vc.widget_name(w).startswith('head')
    #@+node:ekr.20140801121720.18083: *4* vc.is_plain_key & is_text_widget
    def is_plain_key(vc,stroke):
        '''Return True if stroke is a plain key.'''
        return vc.k.isPlainKey(stroke)
        
    def is_text_widget(vc,w=None):
        '''Return True if w is a text widget.'''
        return vc.is_body(w) or vc.is_head(w) or g.app.gui.isTextWidget(w)
    #@+node:ekr.20140805064952.18153: *4* vc.on_idle (no longer used)
    def on_idle(vc,tag,keys):
        '''The idle-time handler for the VimCommands class.'''
        c = keys.get('c')
        if c and vc == c.vimCommands:
            # Call set_border only for the presently selected tab.
            try:
                # Careful: we may not have tabs.
                w = g.app.gui.frameFactory.masterFrame
            except AttributeError:
                w = None
            if w:
                i = w.indexOf(c.frame.top)
                if i == w.currentIndex():
                    vc.set_border()
            else:
                vc.set_border()
    #@+node:ekr.20140801121720.18079: *4* vc.on_same_line
    def on_same_line(vc,s,i1,i2):
        '''Return True if i1 and i2 are on the same line.'''
        # Ensure that i1 <= i2 and that i1 and i2 are in range.
        if i1 > i2: i1,i2 = i2,i1
        if i1 < 0: i1 = 0
        if i1 >= len(s): i1 = len(s)-1
        if i2 < 0: i2 = 0
        if i2 >= len(s): i2 = len(s)-1
        if s[i2] == '\n': i2 = max(0,i2-1)
        return s[i1:i2].count('\n') == 0
    #@+node:ekr.20140802225657.18022: *4* vc.oops
    def oops(vc,message):
        '''Report an internal error'''
        g.warning('Internal vim-mode error: %s' % message)
        
    #@+node:ekr.20140802120757.18001: *4* vc.save_body (handles undo)
    def save_body(vc):
        '''Undoably preserve any changes to body text.'''
        trace = False and not g.unitTesting
        c = vc.c
        w = vc.command_w or vc.w
        name = c.widget_name(w)
        if trace: g.trace(name,g.callers())
        if w and name.startswith('body'):
            # Similar to selfInsertCommand.
            oldSel = vc.old_sel or w.getSelectionRange()
            oldText = c.p.b
            newText = w.getAllText()
            # To do: set undoType to the command spelling?
            if newText != oldText:
                if trace: g.trace('** changed **')
                # undoType = ''.join(vc.command_list) or 'Typing'
                c.frame.body.onBodyChanged(undoType='Typing',
                    oldSel=oldSel,oldText=oldText,oldYview=None)
    #@+node:ekr.20140804123147.18929: *4* vc.set_border & helper
    def set_border(vc,kind=None,w=None,activeFlag=None):
        '''
        Set the border color of vc.w, depending on state.
        Called from qtBody.onFocusColorHelper and vc.show_status.
        '''
        if not w: w = g.app.gui.get_focus()
        if not w: return
        w_name = vc.widget_name(w)
        if w_name == 'richTextEdit':
            vc.set_property(w,focus_flag=activeFlag in (None,True))
        elif w_name.startswith('head'):
            vc.set_property(w,True)
        elif w_name != 'richTextEdit':
            # Clear the border in the body pane.
            try:
                w = vc.c.frame.body.bodyCtrl.widget
                vc.set_property(w,False)
            except Exception:
                pass
    #@+node:ekr.20140807070500.18161: *5* vc.set_property
    def set_property(vc,w,focus_flag):
        '''Set the property of w, depending on focus and state.'''
        trace = False and not g.unitTesting
        selector = 'vim_%s' % (vc.state) if focus_flag else 'vim_unfocused'
        if trace: g.trace(vc.widget_name(w),selector)
        w.setProperty('vim_state',selector)
        w.style().unpolish(w)
        w.style().polish(w)
    #@+node:ekr.20140222064735.16615: *4* vc.show_status
    def show_status(vc):
        '''Show vc.state and vc.command_list'''
        trace = False and not g.unitTesting
        k = vc.k
        vc.set_border()
        if k.state.kind:
            if trace: g.trace('*** in k.state ***',k.state.kind)
        elif False: ### vc.state == 'visual':
            s = '%8s:' % vc.state.capitalize()
            if trace: g.trace('(vimCommands)',s,g.callers())
            k.setLabelBlue(label=s,protect=True)
        else:
            state_s = vc.state.capitalize()
            command_s = vc.show_command()
            dot_s = vc.show_dot()
            # if vc.in_motion: state_s = state_s + '(in_motion)'
            if 1: # Don't show the dot:
                s = '%8s: %s' % (state_s,command_s)
            else:
                s = '%8s: %-5s dot: %s' % (state_s,command_s,dot_s)
            if trace: g.trace('(vimCommands)',s,g.callers(2))
            k.setLabelBlue(label=s,protect=True)
    #@+node:ekr.20140801121720.18080: *4* vc.to_bol & vc.eol
    def to_bol(vc,s,i):
        '''Return the index of the first character on the line containing s[i]'''
        if i >= len(s): i = len(s)
        while i > 0 and s[i-1] != '\n':
            i -= 1
        return i
        
    def to_eol(vc,s,i):
        '''Return the index of the last character on the line containing s[i]'''
        while i < len(s) and s[i] != '\n':
            i += 1
        return i
    #@+node:ekr.20140805064952.18152: *4* vc.widget_name
    def widget_name(vc,w):
        return vc.c.widget_name(w)
    #@-others
#@-others
#@-leo
