import React, { useMemo, useEffect, useState } from 'react';
import { useTable } from 'react-table';
import { parse } from 'papaparse';
import { Box } from '@mui/system';

function Item(props) {
  const { sx, ...other } = props;
  return (
    <Box
      sx={{
        p: 1,
        m: 1,
        ...sx,
      }}
      {...other}
    />
  );
}

function downloadCsv() {
    fetch('/get_csv', {
        method: 'GET',
    })
    .then(response => response.blob())
    .then(blob => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = "data.csv";
      document.body.appendChild(a);
      a.click();  // Simulate click to download
      a.remove();  // Clean up
      window.URL.revokeObjectURL(url);
    })
    .catch(err => console.error("Error while downloading CSV:", err));
};

export default function CsvTableView() {
  const [tableData, setTableData] = useState([]);
  const [buttonText, setButtonText] = useState('Download CSV');

  useEffect(() => {
    fetch('/get_csv', {
        method: 'GET',
    })
      .then(response => response.text())
      .then(csv => {
        const parsedCsv = parse(csv, { header: true, skipEmptyLines: true });
        setTableData(parsedCsv.data);
      })
      .catch(err => console.error("Error loading the CSV data: ", err));
  }, []);

  const data = useMemo(() => tableData, [tableData]);
  const columns = useMemo(() => tableData[0] ? Object.keys(tableData[0]).map(key => ({
    Header: key,
    accessor: key
  })) : [], [tableData]);

  const tableInstance = useTable({ columns, data });
  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = tableInstance;

  const handleDownloadCsv = () => downloadCsv();

  return (
    <div>
      <Box sx={{
          display: 'flex',
          flexWrap: 'nowrap',
          justifyContent: 'flex-end'
        }}>
          <Item>
            <button
              type='submit'
              className='btn'
              tabIndex={0}
              onClick={handleDownloadCsv}
            >
              {buttonText}
            </button></Item>
      </Box>
      <table {...getTableProps()}>
        <thead>
          {headerGroups.map(headerGroup => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map(column => (
                <th {...column.getHeaderProps()}>{column.render('Header')}</th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {rows.map(row => {
            prepareRow(row);
            return (
              <tr {...row.getRowProps()}>
                {row.cells.map(cell => (
                  <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};
