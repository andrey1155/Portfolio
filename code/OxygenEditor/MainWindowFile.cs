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

namespace Editor
{
    public partial class MainWindow
    {
        private void QSave(object sender, ExecutedRoutedEventArgs e)
        {
            if (selectedTabItem.FullPath == "")
            {
                Save(null, null);
                return;
            }

            RichTextBox box = selectedTabItem.Content;
            //RichTextBox box = (RichTextBox)((ActionTabItem)TabControll.Items[TabControll.Items.Count - 1]).Content;
            FileStream fileStream = new FileStream(selectedTabItem.FullPath, FileMode.Create);
            TextRange range = new TextRange(box.Document.ContentStart, box.Document.ContentEnd);          
            range.Save(fileStream, DataFormats.Text);
            fileStream.Close();
            selectedTabItem.IsChanged = false;
        }

        private void Save(object sender, ExecutedRoutedEventArgs e)
        {
            SaveFileDialog dialog = new SaveFileDialog();
            dialog.Filter = "(*.asm)|*.asm";

            if (dialog.ShowDialog() == true)
            {
                RichTextBox box = selectedTabItem.Content;
                //RichTextBox box = (RichTextBox)((ActionTabItem)TabControll.Items[TabControll.Items.Count - 1]).Content;
                FileStream fileStream = new FileStream(dialog.FileName, FileMode.Create);
                TextRange range = new TextRange(box.Document.ContentStart, box.Document.ContentEnd);
                range.Save(fileStream, DataFormats.Text);
                fileStream.Close();
                selectedTabItem.IsChanged = false;
            }
        }

        private void Open(object sender, ExecutedRoutedEventArgs e)
        {
            OpenFileDialog dialog = new OpenFileDialog();
            dialog.Filter = "(*.asm)|*.asm";

            if (dialog.ShowDialog() == true)
            {
                Open(dialog.FileName);
            }
        }

        private void Save(object sender, RoutedEventArgs e)
        {
            SaveFileDialog dialog = new SaveFileDialog();
            dialog.Filter = "(*.asm)|*.asm";

            if (dialog.ShowDialog() == true)
            {
                RichTextBox box = selectedTabItem.Content;
                //RichTextBox box = (RichTextBox)((ActionTabItem)TabControll.Items[TabControll.Items.Count - 1]).Content;
                FileStream fileStream = new FileStream(dialog.FileName, FileMode.Create);
                TextRange range = new TextRange(box.Document.ContentStart, box.Document.ContentEnd);
                range.Save(fileStream, DataFormats.Text);
                fileStream.Close();
                selectedTabItem.IsChanged = false;
            }
        }

        private void Open(string path)
        {
            foreach (var i in vmd.Tabs)
            {
                if (i.FullPath == path)
                {
                    TabControll.SelectedItem = i;
                    return;
                }
            }

            AddTab(path);
            RichTextBox box = selectedTabItem.Content;

            FileStream fileStream = new FileStream(path, FileMode.Open);
            TextRange range = new TextRange(box.Document.ContentStart, box.Document.ContentEnd);
            range.Load(fileStream, DataFormats.Text);
            fileStream.Close();

            TextChanged(null, null);
            selectedTabItem.IsChanged = false;
        }

        private void ShowUnsavedWarning(object sender, System.ComponentModel.CancelEventArgs e)
        {
            List<ActionTabItem> unsaved = new List<ActionTabItem>();
            foreach(var i in vmd.Tabs)
            {
                if (i.IsChanged)
                {
                    unsaved.Add(i);
                }
            }

            if (unsaved.Count == 0)
            {
                return;
            }

            UnsavedWarning T = new UnsavedWarning(unsaved);
            T.ShowDialog();

            if (T.IsOperationCanceled)
                e.Cancel = true;
        }
    }
}
