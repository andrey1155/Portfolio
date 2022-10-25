using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace Editor
{
    /// <summary>
    /// Логика взаимодействия для UnsavedWarning.xaml
    /// </summary>
    public partial class UnsavedWarning : Window
    {
        private List<ActionTabItem> unsaved;
        public bool IsOperationCanceled = false;
        private bool closedByCode = false;
        public UnsavedWarning(List<ActionTabItem> unsaved)
        {
            InitializeComponent();
            this.unsaved = unsaved;

            foreach(var i in this.unsaved)
            {
                Unsaved.Text += i.Header + '\n';
            }
        }

        private void Save(object sender, RoutedEventArgs e)
        {
            foreach (var i in unsaved)
            {
                RichTextBox box = i.Content;
                FileStream fileStream = new FileStream(i.FullPath, FileMode.Create);
                TextRange range = new TextRange(box.Document.ContentStart, box.Document.ContentEnd);
                range.Save(fileStream, DataFormats.Text);
                fileStream.Close();
            }
            closedByCode = true;
            Close();
        }

        private void NoSave(object sender, RoutedEventArgs e)           
        {
            closedByCode = true;
            Close();
        }

        private void Cancel(object sender, RoutedEventArgs e)          
        {
            closedByCode = true;
            IsOperationCanceled = true;
            Close();
        }

        private void Close(object sender, EventArgs e)
        {
            if(!closedByCode)
                IsOperationCanceled = true;
        }
    }
}
