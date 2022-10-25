using System;
using System.Linq;
using System.Collections.Generic;
using System.IO;
using System.Windows;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using Microsoft.Win32;
using System.Windows.Controls;
using Editor;
using System.Diagnostics;
using System.Collections.ObjectModel;
using System.Text.RegularExpressions;
using System.Linq;



namespace Editor
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        Color UsualColor = Colors.White;
        Color InstrColor = Colors.Orange;
        Color RegColor = Colors.OrangeRed;
        Color SpecWordColor = Colors.Blue;
        Color NumColor = Colors.White;
        Color DirectiveColor = Colors.Violet;
        Color CharColor = Colors.DarkGreen;
        Color StringColor = Colors.DarkGreen;
        Color ComentColor = Colors.Gray;

        Color ForegroundColor = (Color)ColorConverter.ConvertFromString("#2E2D38");
        Color BackgroundColor = (Color)ColorConverter.ConvertFromString("#4D455C");
        double defaultFontSize = 18;




        ActionTabItem selectedTabItem
        {
            get { return ((ActionTabItem)TabControll.SelectedContent); }
        }

        public ActionTabItem getSelectedTabItem()
        {
            return((ActionTabItem)TabControll.SelectedContent);
        }

        void SetColors()
        {
            Output.Foreground = new SolidColorBrush(UsualColor);
            Output.FontSize = defaultFontSize;
        }

        private ActionTabViewModel vmd;
        private TreeViewModel tvm;
        private ErrorViewModel evm;

        private DirectoryInfo workingDirectory;

        private List<ASMError> lastCompileErrors = new List<ASMError>();

        public ObservableCollection<ErrorNode> MyCommands { get; set; }

        public MainWindow()
        {
            InitializeComponent();
            SetColors();
            workingDirectory = new DirectoryInfo(System.AppDomain.CurrentDomain.BaseDirectory);

            vmd = new ActionTabViewModel();
            TabControll.ItemsSource = vmd.Tabs;

            tvm = new TreeViewModel();
            DirectoryManager.ItemsSource = tvm.nodes;

            evm = new ErrorViewModel();

            workingDirectory = new DirectoryInfo(System.AppDomain.CurrentDomain.BaseDirectory);
            SetDirectoryManager();

            Closing += ShowUnsavedWarning;
        }

        private void TextChangedNew(object sender, TextChangedEventArgs e)
        {
            if ((ActionTabItem)TabControll.SelectedContent == null)
                return;

            RichTextBox rtbEditor = ((ActionTabItem)TabControll.SelectedContent).Content;

            if (rtbEditor == null)
                return;

            ActionTabItem active = (ActionTabItem)TabControll.SelectedItem;
            active.IsChanged = true;
            setStringsCounter(active.Counter, CountLines(active.Content));

            rtbEditor.TextChanged -= TextChangedNew;

            List<Lexer.Token> tokens = new List<Lexer.Token>();
            var changes = e.Changes;
            //var tp = selectedTabItem.Content.GetP
            string text;
            foreach(var i in e.Changes)
            {
                var tp = selectedTabItem.Content.Document.ContentStart.GetPositionAtOffset(i.Offset);
                if(tp.Parent is Run)
                {
                    text = ((Run)tp.Parent).Text;
                    if (text != "")
                    {
                        Lexer l = new Lexer((Run)tp.Parent);
                        tokens.AddRange(l.lex());
                    }
                }
            }
            foreach (Lexer.Token t in tokens)
            {
                TextRange range = new TextRange(t.StartPosition, t.EndPosition);
                range.ApplyPropertyValue(TextElement.ForegroundProperty, new SolidColorBrush(GetWordColor(t)));
            }
            rtbEditor.TextChanged += TextChangedNew;

        }

        private void TextChanged(object sender, TextChangedEventArgs e)
        {

            if ((ActionTabItem)TabControll.SelectedContent == null)
                return;

            RichTextBox rtbEditor = ((ActionTabItem)TabControll.SelectedContent).Content;

            if (rtbEditor == null)
                return;

            ActionTabItem active = (ActionTabItem)TabControll.SelectedItem;
            active.IsChanged = true;
            setStringsCounter(active.Counter, CountLines(active.Content));
               
            string text;
            TextRange documentRange = new TextRange(rtbEditor.Document.ContentStart, rtbEditor.Document.ContentEnd);
            documentRange.ClearAllProperties();
            documentRange.ApplyPropertyValue(TextElement.ForegroundProperty, new SolidColorBrush(UsualColor));

            List<Lexer.Token> tokens = new List<Lexer.Token>();

            TextPointer navigator = rtbEditor.Document.ContentStart;
            while (navigator.CompareTo(rtbEditor.Document.ContentEnd) < 0)
            {
                TextPointerContext context = navigator.GetPointerContext(LogicalDirection.Backward);
                if (context == TextPointerContext.ElementStart && navigator.Parent is Run)
                {

                    text = ((Run)navigator.Parent).Text;
                    if (text != "")
                    {
                        Lexer l = new Lexer((Run)navigator.Parent);
                        tokens.AddRange(l.lex());
                    }


                }
                navigator = navigator.GetNextContextPosition(LogicalDirection.Forward);
            }


            foreach (Lexer.Token t in tokens)
            {
                TextRange range = new TextRange(t.StartPosition, t.EndPosition);
                range.ApplyPropertyValue(TextElement.ForegroundProperty, new SolidColorBrush(GetWordColor(t)));
            }

        }


        private void AddTab(string name)
        {
            vmd.AddTab(name, TextChangedNew, defaultFontSize, TabControll);
        }

        

        private Color GetWordColor(Lexer.Token token)
        {
            if (token.type == Lexer.Ttype.Instr)
            {
                return InstrColor;
            }
            if (token.type == Lexer.Ttype.Reg)
            {
                return RegColor;
            }
            if (token.type == Lexer.Ttype.Spc)
            {
                return SpecWordColor;
            }
            if (token.type == Lexer.Ttype.Dir)
            {
                return DirectiveColor;
            }
            if (token.type == Lexer.Ttype.Str)
            {
                return StringColor;
            }
            if (token.type == Lexer.Ttype.Chr)
            {
                return CharColor;
            }
            if (token.type == Lexer.Ttype.Num)
            {
                return NumColor;
            }
            if (token.type == Lexer.Ttype.Com)
            {
                return ComentColor;
            }

            return UsualColor;
        }

        private void OpenViewWindow(object sender, RoutedEventArgs e)
        {

        }

        private void Run(object sender, RoutedEventArgs e)
        {
            if (selectedTabItem.FullPath == "")
                return;

            //compile
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = "python.exe";
            start.Arguments = "main.py " + '"' + selectedTabItem.FullPath + '"' + " out.obj -e";
            start.RedirectStandardOutput = true;
            start.RedirectStandardError = true;

            Process process = Process.Start(start);

            //errors?

            StreamReader stdout = process.StandardOutput;
            StreamReader stderr = process.StandardError;
            process.WaitForExit();
            string output = stdout.ReadToEnd();
            string err = stderr.ReadToEnd();

            if (err != "")
            {
                MessageBox.Show(err);
                return;
            }

            ParceErrors(output);

            //run vm

            if(lastCompileErrors.Count == 0)
            {
                Process.Start("OxygenVM v_3.exe", "out.obj");
            }

           
        }


        private void SetDirectoryManager()
        {
            DirectoryManager.ItemsSource = MyDirectoryManager.getFolderData(workingDirectory);
        }

       

        private void TabCloseClick(object sender, MouseButtonEventArgs e)
        {
            if (((ActionTabItem)TabControll.SelectedItem).IsChanged)
            {
                UnsavedWarning T = new UnsavedWarning(new List<ActionTabItem> { (ActionTabItem)TabControll.SelectedItem });
                T.ShowDialog();

                if (T.IsOperationCanceled)
                    return;
            }

            vmd.Tabs.RemoveAt(TabControll.SelectedIndex);
        }


        private void ScrollChange(object sender, ScrollChangedEventArgs e)
        {
            ActionTabItem active = (ActionTabItem)TabControll.SelectedItem;

            active.Counter.ScrollToVerticalOffset(e.VerticalOffset);
        }

        public int CountLines(RichTextBox rtb)
        {
            TextRange documentRange = new TextRange(rtb.Document.ContentStart, rtb.Document.ContentEnd);

            string[] T = documentRange.Text.Split('\r');

            return T.Length - 1;
        }

        private int prev_lines_count = 0;
        private void setStringsCounter(RichTextBox LineCounter, int lines)
        {
            if (lines == prev_lines_count)
                return;

            TextRange documentRange = new TextRange(LineCounter.Document.ContentStart, LineCounter.Document.ContentEnd);
            prev_lines_count = lines;

            if (lines > prev_lines_count)
            {               
                
                for (int i = prev_lines_count+1; i <= lines; i++)
                {
                    documentRange.Text += i.ToString() + "\n";
                }
                return;
            }

            documentRange.Text = "";

            for (int i = 1; i <= lines; i++)
            {
                documentRange.Text += i.ToString() + "\n";
            }
        }

        private void SelectDirectory(object sender, RoutedEventArgs e)
        {
            var T = new DirectorySelector(ref workingDirectory);
            T.ShowDialog();
            workingDirectory = T.directory;

            SetDirectoryManager();
        }

        private void SelectorMouseDown(object sender, MouseButtonEventArgs e)
        {
            if (e.ClickCount != 2)
                return;

            TreeNode selectedItem = (TreeNode)DirectoryManager.SelectedItem;
            FileInfo file = new FileInfo(selectedItem.path + @"\" + selectedItem.FileName);

            if (!file.Exists)
                return;

            string fileName = file.FullName;

            Regex filter = new Regex(@"\S(.asm)$");

            if (filter.IsMatch(fileName))
            {
                Open(fileName);
            }
        }

        private string GetCurrentWord()
        {
            RichTextBox activeBox = ((ActionTabItem)TabControll.SelectedItem).Content;
            TextRange range = new TextRange(activeBox.CaretPosition.GetNextContextPosition(LogicalDirection.Backward), activeBox.CaretPosition);

            string text = range.Text;
            int len = text.Length - 1;

            if (len < 0)
                return "";


            while(len >= 0 && text[len] != ' ')
            {
                len--;
            }
            len++;
            return text.Substring(len, (text.Length - len));

        }
        
        private void ParceErrors(string stdoutput)
        {
            lastCompileErrors.Clear();
            string[] lines = stdoutput.Split("\n\r".ToCharArray(),StringSplitOptions.RemoveEmptyEntries);
            Output.Text = "";
            int len = 0;
            int.TryParse(lines[0], out len);

            for (int i = 0; i < len; i++)
            {
                string err_text = $"{i+1}. " + lines[1 + 3 * i];

                int err_line = 0;
                int.TryParse(lines[1 + 3 * i + 1], out err_line);

                string err_file = lines[1 + 3 * i + 2];

                lastCompileErrors.Add(new ASMError(err_text, err_file, err_line, this));
            }

            foreach(ASMError i in lastCompileErrors)
            {
                Output.Text += i._err + "\n";
            }
        }

        public class ASMError
        {
            public string _err { get; private set; }
            public int _line { get; private set; }
            public string _file { get; private set; }

            private MainWindow mainWindow;




            public ASMError(string e, string f, int l, MainWindow mw)
            {
                _err = e;
                _line = l;
                _file = f;
                mainWindow = mw;
            }

            public void CompilerOutputClick(object sender, RoutedEventArgs e)
            {
                var tab = mainWindow.selectedTabItem;              
            }
        }

        

    }


    public class ErrorViewModel
    {
        public ObservableCollection<ErrorNode> nodes { get; set; }

        public ErrorViewModel()
        {
            nodes = new ObservableCollection<ErrorNode>();
        }
    }

    public class ErrorCommand : ICommand
    {
        public event EventHandler CanExecuteChanged;

        public bool CanExecute(object parameter)
        {
            return true;
        }

        public void Execute(object parameter)
        {
            //activa panel, Error info
            MessageBox.Show("A");
        }
    }

    public class ErrorNode
    {
        public ICommand Command { get; set; }
        public string FileName { get; set; }
        public string Error { get; set; }
        public int Line { get; set; }

    }

    public class TreeNode{
        public string FileName { get; set; }
        public string path { get; set; }
        public ObservableCollection<TreeNode> files { get; set; }
    }

    public class TreeViewModel
    {
        public ObservableCollection<TreeNode> nodes;

        public TreeViewModel()
        {
            nodes = new ObservableCollection<TreeNode>();
        }     
    }

    public class ActionTabItem
    {
        private string header = "";
        private bool _isChanged = false;
        public string ActualHeader
        {
            get
            {
                if (_isChanged)
                    return header + "*";
                else
                    return header;
            }
            set
            {
                header = value;
            }
        }

        public bool IsChanged { get { return _isChanged; } 
            set { _isChanged = value; } }
        public string FullPath { get ; set; }
        public string Header { get; set; }

        public RichTextBox Content { get; set; }
        public RichTextBox Counter { get; set; }
    }

    public class ActionTabViewModel
    {
        public ObservableCollection<ActionTabItem> Tabs { get; set; }

        public ActionTabViewModel()
        {
            Tabs = new ObservableCollection<ActionTabItem>();
        }
        public void AddTab(string path, TextChangedEventHandler textChanged, double fontSize, TabControl parent)
        {
            var main = new RichTextBox();
            main.TextChanged += textChanged;
            main.FontSize = fontSize;

            var lineCounter = new RichTextBox();
            lineCounter.FontSize = fontSize;
            lineCounter.IsReadOnly = true;
            lineCounter.SelectionBrush = new SolidColorBrush(Colors.Transparent);
            lineCounter.Foreground = new SolidColorBrush(Colors.White);

            FileInfo fileInfo = new FileInfo(path);

            var tab = new ActionTabItem { ActualHeader = fileInfo.Name, Header = fileInfo.Name, FullPath = path, Content = main, Counter = lineCounter };
            Tabs.Add(tab);
            parent.SelectedItem = tab;
        }
    }
}
