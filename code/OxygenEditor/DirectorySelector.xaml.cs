using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
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
    /// Логика взаимодействия для DirectorySelector.xaml
    /// </summary>
    public partial class DirectorySelector : Window
    {
        public DirectoryInfo directory;
        private DirectoryInfo start;
        public DirectorySelector(ref DirectoryInfo start)
        {
            InitializeComponent();
            DirectoryManager.ItemsSource = MyDirectoryManager.getFolderData(start);
            directory = start;
            this.start = start;
        }



        private void Aply(object sender, RoutedEventArgs e)
        {
            Close();
        }

        private void Cancel(object sender, RoutedEventArgs e)
        {
            directory = start;
            Close();
        }


        private void Up(object sender, RoutedEventArgs e)
        {
            directory = directory.Parent;
            DirectoryManager.ItemsSource = MyDirectoryManager.getFolderData(directory);
        }

        private void SelectorMouseDown(object sender, MouseButtonEventArgs e)
        {
            if (e.ClickCount != 2)
                return;

            TreeNode selectedItem = (TreeNode)DirectoryManager.SelectedItem;
            directory = new DirectoryInfo(selectedItem.path + @"\" + selectedItem.FileName);

            DirectoryManager.ItemsSource = MyDirectoryManager.getFolderData(directory);
        }
    }

    public static class MyDirectoryManager
    {
        public static ObservableCollection<TreeNode> getFolderData(DirectoryInfo directory)
        {
            ObservableCollection<TreeNode> ret = new ObservableCollection<TreeNode>();

            DirectoryInfo[] fi = directory.GetDirectories();
            for (int i = 0; i < fi.Length; i++)
            {
                TreeNode newObject = new TreeNode { FileName = fi[i].Name,path = fi[i].Parent.FullName };
                newObject.files = getFolderData(fi[i]);
                ret.Add(newObject);
            }


            FileInfo[] file_i = directory.GetFiles();

            for (int i = 0; i < file_i.Length; i++)
            {
                TreeNode newObject = new TreeNode { FileName = file_i[i].Name, path = file_i[i].DirectoryName };
                ret.Add(newObject);
            }

            return ret;
        }
    }
}
